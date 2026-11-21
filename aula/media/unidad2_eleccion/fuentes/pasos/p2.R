ggplot(compo, aes(x = area, y = personas,
                  fill = situacion)) +
  geom_col(position = "fill") +
  scale_y_continuous(
    labels = scales::label_percent()) +
  scale_fill_manual(values = colores) +
  coord_flip() +
  labs(title = "Situación de ocupación, 2025",
       x = NULL, y = "Porcentaje de la población de 15+",
       fill = NULL) +
  theme_minimal(base_size = 11)
