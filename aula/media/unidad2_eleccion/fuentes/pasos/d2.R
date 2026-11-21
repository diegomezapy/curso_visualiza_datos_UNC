ggplot(eph, aes(x = ingreso)) +
  geom_histogram(bins = 40, fill = "#0072B2") +
  scale_x_log10(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  labs(title = "Ingreso mensual de los ocupados",
       x = "Guaraníes (escala logarítmica)",
       y = "Personas (muestra)") +
  theme_minimal(base_size = 11)
