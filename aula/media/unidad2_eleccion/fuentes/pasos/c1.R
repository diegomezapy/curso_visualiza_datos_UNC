ggplot(dptos, aes(x = dpto, y = ingreso_mediano)) +
  geom_col(fill = "#0072B2") +
  labs(title = "Ingreso mediano por departamento",
       x = NULL, y = "Guaraníes") +
  theme_minimal(base_size = 11)
