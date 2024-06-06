my_get_pdf <- function(doi, path = ".", filename = "", overwrite = FALSE){
  
  ## Check args ----
  if (missing(doi)) {
    stop("Argument 'doi' is required", call. = FALSE)
  }
  
  if (!is.logical(overwrite) || length(overwrite) != 1) {
    stop("Argument 'overwrite' must be 'TRUE' or 'FALSE'", call. = FALSE)
  }
  
  base_url <- Sys.getenv("SCIHUB_URL")
  if (base_url == "") {
    stop("You must store the Sci-Hub URL in the '~/.Renviron' file under the ",
         "key 'SCIHUB_URL'", call. = FALSE)
  }
  base_url <- ifelse(endsWith(base_url, "/"), sub("/$", "", base_url), base_url)
  
  ## Get destination file path
  if(!endsWith(filename,".pdf")){
    filename <- paste0(filename, ".pdf")
  }
  file_path <- file.path(path, filename)
  
  
  ## Get HTML page ----
  
  page    <- httr::GET(paste0(base_url,"/", doi))

    
    ## Extract pdf link ----
    
    pdf_link <- rvest::read_html(page) |> 
      rvest::html_elements("button") |> 
      rvest::html_attr("onclick")
    
    if(length(pdf_link) == 0){
      message("No PDF found.")
      return(invisible(NULL))
    }
    
    
    ## Clean pdf link ----
    
    pdf_link <- gsub("location.href=", "", pdf_link)
    pdf_link <- gsub("^'|'$", "", pdf_link)
    pdf_link <- gsub("\\?download=true", "", pdf_link) ## had this commented out before?
    pdf_link <- ifelse(startsWith(pdf_link,"/"), sub(".", "", pdf_link), pdf_link)
    
    
    ## Build URL ----
    
    if (length(grep("^//", pdf_link)) == 1) {
      
      pdf_link <- paste0("https:", pdf_link)  
      
    } else {
      
      pdf_link <- paste(base_url, pdf_link, sep="/")
    }
    
    
    ## Download PDF ----
    
    errorMessage <- try(curl::curl_download(pdf_link, file_path), silent=TRUE)
    
    if(length(grepl("error", errorMessage, ignore.case = TRUE))==0){
      message("No PDF found.")
      return(invisible(NULL))
    }else if(grepl("error", errorMessage, ignore.case = TRUE)){
      message("No PDF found.")
      return(invisible(NULL))
    }else{
      curl::curl_download(pdf_link, destfile = file_path)
      return(invisible(pdf_link))
    }
    

  
}