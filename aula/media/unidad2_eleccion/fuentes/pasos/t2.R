ggplot(tasa, aes(x = anio, y = tasa,
                 color = sexo)) +
  geom_line(linewidth = 1.1) +
  geom_point(size = 2.5) +
  geom_text(data = filter(tasa, anio == 2025),
            aes(label = sexo), hjust = -0.15,
            show.legend = FALSE) +
  scale_color_manual(values = c(Hombres = "#0072B2",
                                Mujeres = "#D55E00")) +
  scale_x_continuous(breaks = 2022:2025,
                     expand = expansion(add = c(0.1, 0.7))) +
  labs(title = "Tasa de ocupación por sexo",
       x = NULL, y = "% de la población de 15+") +
  theme_minimal(base_size = 11) +
  theme(legend.position = "none")
