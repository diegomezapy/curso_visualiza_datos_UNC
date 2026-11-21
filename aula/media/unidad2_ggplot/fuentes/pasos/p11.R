ocup_larga <- ocup_larga |>
  mutate(etiqueta = scales::number(
    personas, big.mark = ".", decimal.mark = ","))

ggplot(data = ocup_larga,
       mapping = aes(x = anio, y = personas,
                     color = ocup)) +
  geom_line() +
  geom_point() +
  geom_text(aes(label = etiqueta), vjust = -0.9,
            size = 3, show.legend = FALSE) +
  scale_x_continuous(breaks = 2022:2025) +
  scale_y_continuous(labels = scales::label_number(
                       big.mark = ".", decimal.mark = ","),
                       expand = expansion(mult = c(0.05, 0.15))) +
  scale_color_manual(values = colores) +
  labs(title = "Concepción: situación de ocupación",
       subtitle = "Estimaciones con factor de expansión",
       x = "Año", y = "Personas estimadas",
       color = "Situación",
       caption = "Fuente: INE, EPHC anual.")
