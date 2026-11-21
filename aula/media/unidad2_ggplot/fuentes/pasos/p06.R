pA <- ggplot(ocup_larga,
             aes(x = anio, y = personas, color = ocup)) +
  geom_point(size = 3) +
  labs(title = "A · color DENTRO de aes()")

pB <- ggplot(ocup_larga, aes(x = anio, y = personas)) +
  geom_point(size = 3, color = "#D55E00") +
  labs(title = "B · color FUERA de aes()")

pA | pB   # patchwork: lado a lado
