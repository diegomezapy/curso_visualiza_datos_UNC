dptos |>
  mutate(foco = dpto == "Concepción") |>
  ggplot(aes(x = ingreso_mediano,
             y = forcats::fct_reorder(dpto, ingreso_mediano),
             fill = foco)) +
  geom_col(show.legend = FALSE) +
  scale_fill_manual(values = c("FALSE" = "#9FB6CB",
                               "TRUE" = "#D55E00")) +
  scale_x_continuous(labels = scales::label_number(
    big.mark = ".", decimal.mark = ",")) +
  labs(title = "Ingreso mediano por departamento",
       x = "Guaraníes", y = NULL) +
  theme_minimal(base_size = 11)
