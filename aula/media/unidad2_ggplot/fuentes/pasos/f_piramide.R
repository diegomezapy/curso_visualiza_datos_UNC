piramide <- piramide |>
  mutate(grupo = forcats::fct_inorder(grupo))

piramide |>
  mutate(n = ifelse(sexo == "Hombres", -personas, personas)) |>
  ggplot(aes(x = grupo, y = n, fill = sexo)) +
  geom_col(width = 0.9) +
  coord_flip() +
  scale_y_continuous(labels = ~ scales::number(
                       abs(.x), big.mark = ".",
                       decimal.mark = ",")) +
  scale_fill_manual(values = c(Hombres = "#0072B2",
                               Mujeres = "#D55E00")) +
  labs(title = "Concepción 2025: población por sexo y edad",
       x = "Grupo de edad", y = "Personas", fill = NULL) +
  theme_minimal()
