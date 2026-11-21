ggplot(ocup_larga,
       aes(x = factor(anio), y = personas,
           fill = ocup)) +
  geom_col(position = "dodge") +
  scale_fill_manual(values = colores) +
  scale_y_continuous(labels = scales::label_number(
                       big.mark = ".", decimal.mark = ",")) +
  labs(x = "Año", y = "Personas estimadas", fill = "Situación") +
  theme_minimal()
