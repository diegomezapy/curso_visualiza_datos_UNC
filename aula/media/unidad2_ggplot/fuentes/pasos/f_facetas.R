ggplot(ocup_larga,
       aes(x = anio, y = personas, color = ocup)) +
  geom_line() + geom_point() +
  scale_x_continuous(breaks = 2022:2025) +
  scale_color_manual(values = colores) +
  facet_wrap(~ ocup, scales = "free_y") +
  theme_minimal() + theme(legend.position = "none")
