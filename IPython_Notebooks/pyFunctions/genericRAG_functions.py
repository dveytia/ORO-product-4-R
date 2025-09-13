class LangchainBGEM3Embeddings(Embeddings):
    def __init__(self, model_name='BAAI/bge-m3', use_fp16=True):
        self.model = BGEM3FlagModel(model_name, use_fp16=use_fp16)

    def embed_documents(self, texts):
        results = self.model.encode(texts, return_dense=True, return_sparse=False)
        dense_vecs = results["dense_vecs"]  # ✅ correct key from the returned dict
        return [vec.tolist() for vec in dense_vecs]

    def embed_query(self, text):
        results = self.model.encode([text], return_dense=True, return_sparse=False)
        dense_vec = results["dense_vecs"][0]
        return dense_vec.tolist()



# extract think tags from the generative Q&A model
def getThinkTag(answer):
    match = re.search(r"<think>(.*?)</think>", answer, re.DOTALL)
    if match:
        extracted_text = match.group(1).strip()
        return extracted_text
    else:
        return None

# extract the answer from the generative Q&A model
def getAnswer(answer):
    split_text = answer.rsplit("</think>", 1)
    if len(split_text) > 1:
        after_think = split_text[1].strip()
        return after_think
    else:
        return None



from typing import Union, List
from langchain.schema import Document
def is_glyph_map(text_or_docs: Union[str, List[Document]], threshold: float = 0.3) -> bool:
    """
    Detects glyph-like corruption from PyPDFLoader output.
    Accepts either a raw text string or a list of LangChain Document objects.
    """
    if isinstance(text_or_docs, list):
        text = "\n".join(doc.page_content for doc in text_or_docs)
    else:
        text = text_or_docs

    lines = text.splitlines()
    if not lines:
        return True

    count_total = len(lines)
    count_glyph_like = sum(bool(re.fullmatch(r'(/?\d+\s*)+', line.strip())) for line in lines)

    ratio = count_glyph_like / count_total
    return ratio > threshold


# load pdfs
def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    if is_glyph_map(pages):
        return None
    return pages

def fallback_load_pdf_excluding_terminal(pdf_path,TERMINAL_SECTIONS = {"references", "reference", "bibliography", "acknowledgement", "acknowledgements"}):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    if is_glyph_map(pages):
        print(f'Fallback [Corrupted content detected] - returning None')
        return None

    output_lines = []
    terminal_triggered = False

    for page in pages:
        lines = page.page_content.splitlines()

        for line in lines:
            stripped = line.strip().lower()
            # Strip leading numbering (e.g., "5. References")
            heading = re.sub(r"^\d+\.?\s*", "", stripped)
            if heading in TERMINAL_SECTIONS:
                terminal_triggered = True
                break
            output_lines.append(line)

        if terminal_triggered:
            break
            
    return "\n".join(output_lines)


## Can also section text using unstructured[pdf]
# Returns a List[Element] present in the pages of the parsed pdf document
def identifyMethods(pdf_path: str,
    method_sections: list = ["methods", "methodology","method","materials and methods"]):
    try:
        elements = partition_pdf(pdf_path)
    except:
        return None
    
    methods_text = ""
    capture = False
    
    for el in elements:
        text = el.text.strip()
        # Normalize and strip leading numbers/punctuation
        normalized_heading = re.sub(r"^\d+\.?\s*", "", text).lower()
        
        if el.category == "Title":
            # if "method" in heading:
            if any(section in normalized_heading for section in method_sections):
                capture = True
            elif capture:
                # Stop when we hit the next title
                break
        elif capture:
            methods_text += el.text + "\n"

    return methods_text.strip()


def clean_text(text: str) -> str:
    # Remove (cid:xx) patterns
    return re.sub(r'\(cid:\d+\)', '', text)

def is_corrupted(text: str) -> bool:
    return '(cid:' in text or len(text.strip()) == 0



def extract_text_excluding_sections(
    pdf_path: str,
    exclude_sections: list = ["methods", "methodology","method","materials and methods", "references", "bibliography","reference"]
) -> str:
        
    filtered_text = []
    skip = False

    for el in elements:
        text = el.text.strip()

        # Normalize and strip leading numbers/punctuation
        normalized_heading = re.sub(r"^\d+\.?\s*", "", text).lower()

        # If it's a title and matches an excluded section, start skipping
        if el.category == "Title":
            if any(section in normalized_heading for section in exclude_sections):
                skip = True
                continue
            else:
                skip = False

        if not skip:
            filtered_text.append(text)

    return "\n".join(filtered_text)



def extract_text_excluding_sections_terminal(
    pdf_path: str,
    exclude_sections: list = ["methods", "methodology","method","materials and methods"],
    TERMINAL_SECTIONS = {"references","reference", "bibliography", "acknowledgement","acknowledgements"}
) -> str:

    try:
        elements = partition_pdf(filename=pdf_path)
    except:
        fallback_text = fallback_load_pdf_excluding_terminal(pdf_path, TERMINAL_SECTIONS)
        return fallback_text
        
    filtered_text = []
    skip = False
    in_terminal_section = False

    for el in elements:
        text = el.text.strip()

        if is_corrupted(text):
            print(f"[Corrupted content detected] Trying fallback...")
            fallback_text = fallback_load_pdf_excluding_terminal(pdf_path, TERMINAL_SECTIONS)
            return fallback_text

        # Normalize and strip leading numbers/punctuation
        normalized_heading = re.sub(r"^\d+\.?\s*", "", text).lower()

        # If it's a title and matches an excluded section, start skipping
        if el.category == "Title":
            if normalized_heading in TERMINAL_SECTIONS:
                in_terminal_section = True
                break  # Stop processing further text altogether
                
            if any(section in normalized_heading for section in exclude_sections):
                skip = True
                continue
            else:
                skip = False

        if in_terminal_section:
            break  # Stop processing all further elements
            
        if not skip:
            filtered_text.append(text)

    return "\n".join(filtered_text)



def is_valid_section_heading(text):
    """Heuristic to reject likely reference citations mistaken as headings."""
    lower = text.lower()

    # Reject if it looks like a citation
    if re.search(r'\b\d{4}\b', lower):  # year
        return False
    if re.search(r'\d+\s*,\s*\d+', lower):  # volume and page
        return False
    if any(term in lower for term in ['journal', 'sci.', 'doi', 'environ.', 'vol.', 'no.']):
        return False
    # if len(text.split()) > 10:  # too long
    #     return False

    return True


    

def split_text(pages, chunk_size = 500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " "]
    )
    chunks = text_splitter.split_documents(pages)
    return chunks

def split_text_unstructured(text=list, chunk_size = 500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " "]
    )
    chunks = text_splitter.create_documents(text)
    return chunks


# If vectors don't exist, get them from embeddings function
def get_vectorstore(text_chunks, embeddings):
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# If vectors exist, load them
def load_vectorstore(faiss_path, embeddings):
    """Load FAISS vectorstore from disk if available."""
    if os.path.exists(faiss_path):
        return FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
    return None


# Retrieve relevant chunks based on similarity to variables
def retrieve_docs(query, vector_store, faissK=4):
    return vector_store.similarity_search(query, k=faissK)



# Chain together  the prompts and models
def format_docs(related_documents):
    return "\n\n".join(doc.page_content for doc in related_documents)

