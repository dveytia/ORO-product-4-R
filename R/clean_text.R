clean_text <- function(text){
  text <- gsub("- ", "-", text)          # Deal with caesura
  text <- gsub("[[:punct:]]", " ", text) # Remove punctuation
  text <- gsub("[0-9]", "", text)        # Remove numbers
  text <- gsub("\\s+", "-", text)        # Remove whitespaces
  text <- gsub("^\\s|\\s$", "-", text)    # Remove whitespaces
  return(text)
}