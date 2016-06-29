library(plotly)
library(reshape2)
library(plyr)
library(RPostgreSQL)


con <- dbConnect(PostgreSQL(), user= "postgres", password="psql", dbname="tagpro")

data = dbGetQuery(con, "SELECT * FROM players;")
data = data[c(-1)]


data$mmr = as.numeric(data$mmr/100)
data$sigma = as.numeric(data$sigma/100)
data$name = as.character(data$name)
data = data[order(data$mmr, decreasing=T),]
nb_joueurs = nrow(data)
colnames(data)[colnames(data)=="name"]="Joueur"
colnames(data)[colnames(data)=="mmr"]="Niveau"
colnames(data)[colnames(data)=="sigma"]="Confiance"

scope = seq(0,59.9,0.1)
data_pour_graphe = data.frame(scope)

for (i in 1:(nb_joueurs)){
  data_pour_graphe[,i+1] = dnorm(scope, mean=data[i,2], sd=data[i,3])
}
colnames(data_pour_graphe)[c(-1)] = data$Joueur
data_pour_graphe=data_pour_graphe[,-1]

data_fondue = melt(data_pour_graphe)
data_fondue$abscisse = rep(scope, nb_joueurs)
colnames(data_fondue)[colnames(data_fondue)=="variable"]="Joueur"
colnames(data_fondue)[colnames(data_fondue)=="value"]="ordonnee"

data_fondue = join(data_fondue, data)
data_fondue$Rang = rep(rank(-unique(data_fondue$Niveau)), each=nrow(data_fondue)/nb_joueurs)

p = ggplot(data=data_fondue, 
           aes(abscisse)) + 
  geom_area(aes(y=ordonnee, fill=Joueur), alpha=0.5, position="identity")+
  xlim(0,60)


plot_creation = plotly_build(p)
for (i in 1:nb_joueurs){
  plot_creation$data[[i]]$text = paste("Joueur : ", data[i, "Joueur"], 
                                       "<br> Niveau estime : ", round(data$Niveau[i], 1),
                                       "<br> Rang : ", i)
}

plot_creation
