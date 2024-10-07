#!/bin/bash
mkdir -p /home/ecommerce/vendas
cp /home/ecommerce/dados_de_vendas.csv /home/ecommerce/vendas/dados_de_vendas.csv
mkdir -p /home/ecommerce/vendas/backup
cp /home/ecommerce/vendas/dados_de_vendas.csv /home/ecommerce/vendas/backup/dados-$(date +%Y%m%d).csv
mv /home/ecommerce/vendas/backup/dados-$(date +%Y%m%d).csv /home/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv
echo "Data e Hora: $(date '+%Y/%m/%d %H:%M')" >> /home/ecommerce/vendas/backup/relatorio.txt
head -n 2 /home/ecommerce/vendas/dados_de_vendas.csv | tail -n 1 | cut -d',' -f5 >> /home/ecommerce/vendas/backup/relatorio.txt
tail -n 1 /home/ecommerce/vendas/dados_de_vendas.csv | cut -d',' -f5 >> /home/ecommerce/vendas/backup/relatorio.txt
tail -n +2 /home/ecommerce/vendas/dados_de_vendas.csv | wc -l >> /home/ecommerce/vendas/backup/relatorio.txt
head /home/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv >> /home/ecommerce/vendas/backup/relatorio.txt
zip -r /home/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).zip /home/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv
rm /home/ecommerce/vendas/backup/backup-dados-$(date +%Y%m%d).csv
rm /home/ecommerce/vendas/dados_de_vendas.csv

