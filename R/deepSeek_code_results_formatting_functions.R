
## FUNCTIONS FOR FORMATTING DEEPSEEK CODING RESULTS



## Rename label values from a mapping list
#' where label_map is a named list, each named element corresponds to the column name in df
#' and each list element is a named vector of c("new label" = "old label")
rename_labels <- function(df, label_map) {
  require(stringi)
  for (varname in names(label_map)) {
    map <- label_map[[varname]]
    
    # fix a trailing space in your map name(s)
    names(map) <- trimws(names(map))
    
    old <- unname(map)      # substrings to find
    new <- names(map)       # replacements
    
    # Single pass per column; fixed (literal) matching; very fast
    df[[varname]] <- stri_replace_all_fixed(
      df[[varname]], old, new, vectorize_all = FALSE
    )
  }
  df
}





expand_labels <- function(df, id_col, list_col) {
  id_col_quo <- enquo(id_col)
  list_col_quo <- enquo(list_col)
  
  df %>%
    mutate(
      parsed_labels = str_replace_all(!!list_col_quo, "^NA$|^'NA'$|^\"NA\"$", "[]"),
      parsed_labels = str_replace_all(parsed_labels, "\\[|\\]", ""),
      parsed_labels = str_split(parsed_labels, ",\\s*"),
      parsed_labels = map(parsed_labels, ~ unique(str_trim(str_replace_all(.x, "^['\"]|['\"]$", ""))))
    ) %>%
    unnest(parsed_labels) %>%
    filter(!is.na(parsed_labels), parsed_labels != "")
}




expand_labels_with_weight <- function(df, id_col, list_col) {
  id_col_quo <- enquo(id_col)
  list_col_quo <- enquo(list_col)
  
  df %>%
    mutate(
      parsed_labels = str_replace_all(!!list_col_quo, "^NA$|^'NA'$|^\"NA\"$", "[]"),
      parsed_labels = str_replace_all(parsed_labels, "\\[|\\]", ""),
      parsed_labels = str_split(parsed_labels, ",\\s*"),
      parsed_labels = map(parsed_labels, ~ unique(str_trim(str_replace_all(.x, "^['\"]|['\"]$", ""))))
    ) %>%
    unnest(parsed_labels) %>%
    filter(!is.na(parsed_labels), parsed_labels != "") %>%
    distinct(!!id_col_quo, parsed_labels) %>%
    group_by(!!id_col_quo) %>%
    mutate(weight = 1 / n()) %>%
    ungroup() %>%
    rename(label = parsed_labels)
}


join_oro_with_label <- function(oro_df, codedVars, label_col, label_levels = NULL, id_col = id) {
  # Convert inputs to symbols and strings
  id_col_quo <- rlang::enquo(id_col)
  label_col_quo <- rlang::enquo(label_col)
  id_col_str <- rlang::as_name(id_col_quo)
  
  # Expand labels with weight
  label_df <- expand_labels_with_weight(codedVars, !!id_col_quo, !!label_col_quo)
  
  # Ensure the ID column exists in both data frames
  if (!(id_col_str %in% colnames(oro_df))) {
    stop(glue::glue("Column '{id_col_str}' not found in oro_df"))
  }
  if (!(id_col_str %in% colnames(label_df))) {
    stop(glue::glue("Column '{id_col_str}' not found in label_df (after label expansion)"))
  }
  
  # Merge and process
  type_label_joined <- merge(
    oro_df, label_df, by = id_col_str, all = TRUE,
    suffixes = c("", "_label")
  ) %>%
    mutate(weight = oro_weight * weight) %>%
    group_by(oro_type, label) %>%
    summarise(
      weightedSum = sum(weight, na.rm = TRUE),
      count = n_distinct(!!id_col_quo),
      oro_weight = sum(oro_weight, na.rm = TRUE),
      .groups = "drop"
    ) %>%
    replace_na(list(label = "None identified")) %>%
    mutate(
      weightedSum = ifelse(is.na(weightedSum), oro_weight, weightedSum),
      oro_type = factor(oro_type, levels = oroTypeAes$levels)
    )
  
  # Optional: reorder factor levels
  if (!is.null(label_levels)) {
    
    if(sum(type_label_joined$label == "None identified", na.rm=T) > 0){
      label_levels = c(label_levels, "None identified")
    }
    
    type_label_joined <- type_label_joined %>%
      mutate(label = factor(label, levels = label_levels))
  }
  
  return(type_label_joined)
}




join_oro_with_multilabels <- function(
    oro_df,
    codedVars,
    label_cols,               # character vector: c("continent", "sector", ...)
    label_levels_list = NULL, # named list: list(continent = c(...), sector = c(...))
    id_col = "id",
    make_summary = TRUE
) {
  id_col_sym <- rlang::sym(id_col)
  
  # Step 1: Expand and collect all label information
  all_labels <- purrr::map(label_cols, function(colname) {
    col_sym <- rlang::sym(colname)
    
    label_df <- expand_labels_with_weight(codedVars, !!id_col_sym, !!col_sym)
    # label_df$label_col <- colname  # tag the source column
    
    
    # Optional: apply factor levels
    if (!is.null(label_levels_list) && colname %in% names(label_levels_list)) {
      levels_this_col <- label_levels_list[[colname]]
      # if ("None identified" %in% label_df$label) {
      levels_this_col <- c(levels_this_col, "None identified")
      # }
      label_df <- label_df %>%
        mutate(label = factor(label, levels = levels_this_col))
    }
    
    colnames(label_df) <- c("id",colname, paste(colname,"weight", sep="_"))
    
    return(label_df)
  })
  all_labels <- purrr::reduce(all_labels, full_join, by = "id")%>%
    mutate(across(
      where(is.character),
      ~replace_na(.x, "None identified")
    )) %>%
    mutate(across(
      where(is.numeric),
      ~replace_na(.x, 1)
    ))
  
  
  # Step 2: Merge with oro and compute weighted sums
  group_cols_sym = c("oro_type", label_cols)
  
  joined <- merge(
    oro_df, all_labels, by = id_col, all = TRUE
  ) %>%
    mutate(
      oro_type = factor(
        oro_type, 
        levels = oroTypeAes$levels
      )
    ) %>%
    rowwise() %>%
    mutate(weight = prod(c_across(contains("weight")))) %>%
    ungroup() %>%
    mutate(across(
      where(is.factor),
      ~replace_na(.x, "None identified")
    ))
    
  if(make_summary){
    joined <- joined %>%
      group_by(across(all_of(group_cols_sym))) %>%
      summarise(weightedSum = sum(weight, na.rm = TRUE), count = n_distinct(id, na.rm=T), .groups = "drop") 
  }
    
  return(joined)
}





join_oro_with_multilabels_long <- function(
    oro_df,
    codedVars,
    label_cols,               # character vector: c("continent", "sector", ...)
    label_levels_list = NULL, # named list: list(continent = c(...), sector = c(...))
    id_col = "id"
) {
  id_col_sym <- rlang::sym(id_col)
  
  # Step 1: Expand and collect all label information
  all_labels <- purrr::map(label_cols, function(colname) {
    col_sym <- rlang::sym(colname)
    
    label_df <- expand_labels_with_weight(codedVars, !!id_col_sym, !!col_sym)
    # label_df$label_col <- colname  # tag the source column
    
    
    # Optional: apply factor levels
    if (!is.null(label_levels_list) && colname %in% names(label_levels_list)) {
      levels_this_col <- label_levels_list[[colname]]
      # if ("None identified" %in% label_df$label) {
      levels_this_col <- c(levels_this_col, "None identified")
      # }
      label_df <- label_df %>%
        mutate(label = factor(label, levels = levels_this_col))
    }
    
    colnames(label_df) <- c("id",colname, paste(colname,"weight", sep="_"))
    
    return(label_df)
  })
  all_labels <- purrr::reduce(all_labels, full_join, by = "id")%>%
    mutate(across(
      where(is.character),
      ~replace_na(.x, "None identified")
    )) %>%
    mutate(across(
      where(is.numeric),
      ~replace_na(.x, 1)
    ))
  
  
  # Step 2: Merge with oro and compute weighted sums
  group_cols_sym = c("oro_type", label_cols)
  
  joined <- merge(
    oro_df, all_labels, by = id_col, all = TRUE
  ) %>%
    mutate(
      oro_type = factor(
        oro_type, 
        levels = oroTypeAes$levels
      )
    ) %>%
    distinct(across(all_of(c("id", group_cols_sym)))) %>%
    mutate(across(
      where(is.factor),
      ~replace_na(.x, "None identified")
    )) 
  
  return(joined)
}



## Old function for rescaling while maintaining positive and negative values
rescale_signed <- function(x) {
  # Start with all NA to preserve missing values
  out <- rep(NA_real_, length(x))
  
  # Separate positives and negatives
  neg_idx <- which(x < 0 & !is.na(x))
  pos_idx <- which(x > 0 & !is.na(x))
  
  # Rescale negatives to (-1, 0)
  if (length(neg_idx) ==1){
    out[neg_idx] <- -1
  }else if (length(neg_idx) > 0) {
    neg <- x[neg_idx]
    out[neg_idx] <- -1 + (neg - min(neg, na.rm = TRUE)) /
      (max(neg, na.rm = TRUE) - min(neg, na.rm = TRUE))
  }
  
  # Rescale positives to (0, 1)
  if (length(pos_idx) == 1){
    out[pos_idx] <- 1
  }else if (length(pos_idx) > 0) {
    pos <- x[pos_idx]
    out[pos_idx] <- (pos - min(pos, na.rm = TRUE)) /
      (max(pos, na.rm = TRUE) - min(pos, na.rm = TRUE))
  }
  
  # Keep zeros as 0
  zero_idx <- which(x == 0 & !is.na(x))
  out[zero_idx] <- 0
  
  out
}

