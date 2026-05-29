---
title: "Strategic Implications"
author: "McAelan Remigio"
format: html
toc: true
embed-resources: TRUE
smooth-scroll: TRUE
---

# libraries
library(ggplot2)
library(dplyr)
library(tidyr)
library(stringr)
library(ggrepel)
library(purrr)
library(table1)
library(knitr)
library(rlang)


# load dataset
df <- read.csv("filepath", stringsAsFactors = FALSE)

# pie chart function
create_pie_chart <- function(df, column_name, title = "Pie Chart Responses") {
  
  # pull values and drop NA/blank
  vals <- df[[column_name]]
  vals <- vals[!is.na(vals) & vals != ""]
  
  if (length(vals) == 0) {
    message(paste0("No non-empty data in column '", column_name, "'."))
    return(invisible(NULL))
  }
  
  # robust counts
  df_counts <- dplyr::tibble(Choice = vals) |>
    dplyr::count(Choice, name = "Count") |>
    dplyr::arrange(dplyr::desc(Count)) |>
    dplyr::mutate(Percent = round(100 * Count / sum(Count), 1),
                  Choice = paste0(Choice, " - ", Count, " (", Percent, "%)"))
  
  ggplot(df_counts, aes(x = "", y = Count, fill = Choice)) +
    geom_bar(width = 1, stat = "identity", color = "black") +
    coord_polar("y", start = 0) +
    theme_void() +
    scale_fill_brewer(palette = "Set3") + 
    labs(title = title) +
    theme(
      plot.title = element_text(hjust = 0.5, size = 14, face = "bold"),
      legend.position = "right", 
      legend.title = element_blank(),
      legend.text = element_text(size = 10)
    )
}


# bar chart
create_bar_chart <- function(df, column_name, title = "Bar Chart Responses") {
  values <- na.omit(df[[column_name]])
  
  df_values <- data.frame(Value = values)
  
  p <- ggplot(df_values, aes(x = Value)) +
    geom_bar(fill = "steelblue") +
    labs(title = title, x = column_name, y = "Count") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
  
  return(p)
}
```

## Regular Pie Chart Function for Categorical
create_pie_chart(df, "vars_n", title="Title (optional)")

# If Skip Case Not Skipped and Change Variable Names
df = df %>% 
  dplyr::mutate(
    updated_var_1 = dplyr::case_when(
      stringr::str_detect(var_1, "1") ~ "1",
      stringr::str_detect(var_1, "2") ~ "2",
      stringr::str_detect(var_1, "3") ~ "3",
      stringr::str_detect(var_1, "4") ~ "4",
      stringr::str_detect(var_1, "5") ~ "5",
      stringr::str_detect(var_1, "6") ~ "6",
      stringr::str_detect(var_1, "Not Set") ~ "Not Set",
      TRUE ~ "Not Set"
    )
  )
create_pie_chart(df, "updated_var_1", title="New Title")

### String Column + Vector for Col Counts
df2 <- df %>%
  rename(feedback_col = old_feedback_col) %>%
  dplyr::select(feedback_col)

# named vector: names become column names, scanned for 
vector_list <- c(
  Name1         = "\\bname1\\b",
  Name2           = "\\bname2\\b",
  Name3         = "\\bname3\\b",
  ...              = "\\...\\b",
  NameN    = "\\bnamen\\b"
)

# NA
txt <- str_to_lower(coalesce(df2$feedback_col, ""))

vector_cols <- lapply(vector_list, function(p) {
  str_detect(txt, regex(p, ignore_case = TRUE))
})

vector_name <- df2 %>%
  bind_cols(as_tibble(vector_cols)) %>%
  mutate(any_vector_name = reduce(across(all_of(names(vector_list))), `|`))

# Tidy counts for each name (descending)
name_counts <- vector_name %>%
  summarise(across(all_of(names(vector_list)), ~ sum(.x, na.rm = TRUE))) %>%
  pivot_longer(everything(), names_to = "name", values_to = "count") %>%
  arrange(desc(count))

# Returns the counts from any data frame + text column
count_names <- function(data, text_col) {
  col_sym <- rlang::ensym(text_col)
  txt <- str_to_lower(coalesce(dplyr::pull(data, !!col_sym), ""))
  vector_cols <- lapply(vector_list, function(p) {
    str_detect(txt, regex(p, ignore_case = TRUE))
  })
  as_tibble(vector_cols) %>%
    summarise(across(everything(), ~ sum(.x, na.rm = TRUE))) %>%
    pivot_longer(everything(), names_to = "name", values_to = "count") %>%
    arrange(desc(count))
}

count_names(df2, feedback_col) %>%
  knitr::kable(align = c("l", "r"), caption = "Name Mentions Count")


table1::table1(~Name1:Name2:Name3:...:table1::setLabel(Name4, "Name 4"):any_vector_name, data = vector_name, caption = "Name Count from Feedback Column")
# name 4 example of setting label

# Filtering for characters
df_filter <- df %>%
  dplyr::filter(stringr::str_detect(tolower(as.character(var_n)), "string"))

df_filter_2 <- df_grad %>%
  dplyr::filter(!is.na(Experiential_Learning) & Experiential_Learning != "")

create_pie_chart(df_grad_el, "String", title = "title")

# Setup for Subsets
df_yes    <- df %>% filter(!is.na(vars) & vars != "")
df_no  <- df %>% filter(is.na(vars) | vars == "")

# flags
df_filter <- df_filter %>%
  mutate(
    insert_variable =
      (!is.na(name_of_one != "") |
      (!is.na(name_of_two != "") |
      (!is.na(name_of_three != "")
  ) %>%
  mutate(has_name_after_flag = ifelse(has_name_after, "Named", "None Named"))

df_el <- df %>% filter(!is.na(a_variable) & a_variable != "")

create_pie_chart(df_grad %>% filter(!is.na(variable) & variable != ""),
                 "has_name_after_flag",
                 title = "Title")
create_pie_chart(df_grad %>% filter(is.na(variable) | variable == ""),
                 "has_name_after_flag",
                 title = "Title (Non)")
