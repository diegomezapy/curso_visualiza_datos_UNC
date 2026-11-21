ggplot(tasa, aes(x = factor(anio), y = tasa,
                 fill = sexo)) +
  geom_col(position = "dodge") +
  coord_cartesian(ylim = c(50, 82)) +
  scale_fill_manual(values = c(Hombres = "#0072B2",
                               Mujeres = "#D55E00")) +
  labs(title = "Tasa de ocupación por sexo",
       x = NULL, y = "% de la población de 15+",
       fill = NULL) +
  theme_minimal(base_size = 11)
