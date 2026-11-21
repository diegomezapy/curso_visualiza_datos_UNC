ggplot(compo, aes(x = "", y = personas,
                  fill = situacion)) +
  geom_col(position = "fill", width = 1) +
  coord_polar(theta = "y") +
  facet_wrap(~ area) +
  scale_fill_manual(values = colores) +
  labs(title = "Situación de ocupación, 2025",
       fill = NULL) +
  theme_void(base_size = 11)
