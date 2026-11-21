colores <- c(Ocupado = "#0072B2",
           Desocupado = "#D55E00",
           Inactivo = "#009E73")

ggplot(data = ocup_larga,
       mapping = aes(x = anio, y = personas,
                     color = ocup)) +
  geom_line() +
  geom_point() +
  scale_x_continuous(breaks = 2022:2025) +
  scale_y_continuous(labels = scales::label_number(
                       big.mark = ".", decimal.mark = ",")) +
  scale_color_manual(values = colores)
