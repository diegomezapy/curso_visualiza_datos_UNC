ggplot(eph, aes(x = area, y = ingreso,
                fill = sexo)) +
  geom_boxplot(outlier.alpha = 0.2) +
  scale_y_log10(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  scale_fill_manual(values = c(Hombres = "#0072B2",
                               Mujeres = "#D55E00")) +
  labs(title = "Ingreso por área y sexo",
       x = NULL, y = "Guaraníes (escala log)",
       fill = NULL) +
  theme_minimal(base_size = 11)
