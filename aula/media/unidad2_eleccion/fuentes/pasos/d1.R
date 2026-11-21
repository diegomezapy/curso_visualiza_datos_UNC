ggplot(eph, aes(x = ingreso)) +
  geom_histogram(fill = "#0072B2") +
  scale_x_continuous(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  labs(title = "Ingreso mensual de los ocupados",
       x = "Guaraníes", y = "Personas (muestra)") +
  theme_minimal(base_size = 11)
