# fase4/analysis.R
# Script R para Análise Exploratória de Dados (Global Solution)
# Disciplina: Linguagem R

# Instalar pacotes se necessário (descomente)
# install.packages("ggplot2")
# install.packages("dplyr")

library(ggplot2)
library(dplyr)

# Ler dados exportados do Python
df <- read.csv("sensor_data.csv")

# Resumo Estatístico
summary(df)

# Gráfico de Dispersão: CO2 vs Luminosidade
png("r_plot_co2_vs_lux.png")
ggplot(df, aes(x=luminosity, y=co2)) +
  geom_point(aes(color=sector), size=3) +
  labs(title="Correlação: Luminosidade vs Emissão de CO2",
       x="Luminosidade (lux)", y="CO2 (kg/ha)") +
  theme_minimal()
dev.off()

print("Análise R concluída! Gráfico salvo.")
