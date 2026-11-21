ggplot(eph, aes(x = anios_est, y = ingreso)) +
  geom_jitter(width = 0.3, height = 0,
              alpha = 0.1, size = 1,
              color = "#9FB6CB") +
  geom_smooth(color = "#D55E00", se = FALSE,
              linewidth = 1.2) +
  scale_y_log10(
    labels = scales::label_number(
      big.mark = ".", decimal.mark = ",")) +
  labs(title = "Educación e ingreso: la tendencia",
       x = "Años de estudio",
       y = "Guaraníes (escala log)") +
  theme_minimal(base_size = 11)
