ggplot(eph, aes(x = anios_est, y = ingreso)) +
  geom_point() +
  scale_y_continuous(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  labs(title = "Educación e ingreso",
       x = "Años de estudio", y = "Guaraníes") +
  theme_minimal(base_size = 11)
