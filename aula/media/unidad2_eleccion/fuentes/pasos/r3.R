ggplot(eph, aes(x = anios_est, y = ingreso)) +
  geom_bin2d(bins = 18) +
  scale_y_log10(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  scale_fill_gradient(low = "#DCE9F5",
                      high = "#0B2E4A") +
  labs(title = "Educación e ingreso",
       x = "Años de estudio",
       y = "Guaraníes (escala log)",
       fill = "Personas") +
  theme_minimal(base_size = 11)
