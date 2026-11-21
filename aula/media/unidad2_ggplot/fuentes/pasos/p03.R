ggplot(data = ocup_larga,
       mapping = aes(x = anio, y = personas,
                     group = ocup)) +
  geom_line()
