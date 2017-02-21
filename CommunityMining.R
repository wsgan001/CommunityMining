library("gplots", lib.loc="/Library/Frameworks/R.framework/Versions/3.3/Resources/library")
library("RColorBrewer", lib.loc="/Library/Frameworks/R.framework/Versions/3.3/Resources/library")
library("WGCNA", lib.loc="/Library/Frameworks/R.framework/Versions/3.3/Resources/library")
library("igraph", lib.loc="/Library/Frameworks/R.framework/Versions/3.3/Resources/library")
setwd('/Users/zhangchi/Desktop/cs690/Project')
AM = as.matrix(read.csv("FinalAdjacencyMatrix.csv",sep=",", header=TRUE, row.names=1)) # sent emails
AMlist = read.csv("FinalAdjacencyMatrix.csv",sep=",", header=TRUE, row.names=1) # sent emails as list
# employee information might be interesting to analyze for considering relationships # within the company
# enronemployees = read.table("Enron Employee Information.csv", sep=",", header=T) AMt = t(AM) # received emails
AM2 <- AM + t(AM) - 2*diag(diag(AM)) # sent and received emails
AM.names=c(rep(NA,20), row.names(AM)[21],rep(NA,44), row.names(AM)[66], rep(NA,2), row.names(AM)[69], rep(NA,87))
heatmap.2(log2(AM+1), Rowv=FALSE, Colv= FALSE, dendrogram="none", col = (brewer.pal(9,"Blues")),scale="none", trace="none",
          labRow=AM.names,labCol=AM.names, colsep=FALSE,
          density="none", key.title="", key.xlab="# of emails (log2 scale)" , mar=c(8,8))

# eigenvalue centrality (on both directed graphs),
# degree, betweenness, and closeness
eng <- graph.adjacency(do.call(rbind,AMlist)) 
engt <- graph.adjacency(do.call(cbind,AMlist))
eigcent <- igraph::evcent(eng, directed=TRUE)
eigcentt <- igraph::evcent(engt, directed=TRUE) # eigenvalue centrality on transpose of graph
dcent <- igraph::degree(eng) 
bmeas <- igraph::betweenness(eng) 
cmeas <- igraph::closeness(eng)
# TOM
AM2 <- AM2 / max(AM2)
TOM <- TOMsimilarity(AM2)
## ..connectivity..
## ..matrix multiplication..
## ..normalization..
## ..done.
# degree centrality
# betweenness
# closeness
# set values between 0 and 1
# create TOM
TOMrank <- as.matrix(apply(TOM,1,sum)) # grab its row-sums 
rownames(TOMrank) <- rownames(AM)
colnames(TOMrank) <- "value"

comptable <- matrix(ncol=6, nrow=dim(AM)[1]) 
comptable[,1] <- rank(dcent)
comptable[,2] <- rank(eigcent$vector) 
comptable[,3] <- rank(eigcentt$vector) 
comptable[,4] <- rank(cmeas)
comptable[,5] <- rank(bmeas) 
comptable[,6] <- rank(TOMrank)
pairs(comptable[,1:6],pch=20,main="Ranking Metrics Comparison",
      labels=c("Degree","EV Cent.", "EV Cent. (T)","Closeness","Betweenness", "TOM"), cex=.5,xlim=c(0,160),ylim=c(0,160),lower.panel=panel.cor)


panel.cor <- function(x, y, digits = 2, prefix = "", cex.cor, ...)
{
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(0, 1, 0, 1))
  r <- abs(cor(x, y))
  txt <- format(c(r, 0.123456789), digits = digits)[1]
  txt <- paste0(prefix, txt)
  if(missing(cex.cor)) cex.cor <- 0.8/strwidth(txt)
  text(0.5, 0.5, txt, cex = cex.cor * r)
}

rankedEnron <- data.frame(Degree = rownames(AM)[order(-dcent)],
                          EVcent = rownames(AM)[order(-eigcent$vector)],
                          EVcentT = rownames(AM)[order(-eigcentt$vector)], Close = rownames(AM)[order(-cmeas)],
                          Between = rownames(AM)[order(-bmeas)],
                          TOM = rownames(AM)[order(-TOMrank)])
rankedEnron[1:10,]