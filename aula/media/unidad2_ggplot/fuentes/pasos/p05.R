ggplot(data = ocup_larga,
       mapping = aes(x = anio, y = personas,
                     color = ocup)) +
  geom_line() +
  geom_point()
