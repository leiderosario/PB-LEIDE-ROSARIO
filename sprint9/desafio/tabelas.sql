-- Criar tabela Dimensão: País
CREATE TABLE Dim_Pais (
    id_pais INT AUTO_INCREMENT PRIMARY KEY,
    nome_pais VARCHAR(100) NOT NULL
);

-- Criar tabela Dimensão: Plataforma
CREATE TABLE Dim_Plataforma (
    id_plataforma INT AUTO_INCREMENT PRIMARY KEY,
    nome_plataforma VARCHAR(100) NOT NULL
);

-- Criar tabela Fato_Desempenho (com mais detalhes)
CREATE TABLE Fato_Desempenho (
    id_fato INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT,
    id_genero INT,
    id_decada INT,
    id_pais INT,
    id_plataforma INT,
    data_lancamento DATE,
    receita BIGINT,
    custo_producao BIGINT,
    numero_espectadores BIGINT,
    nota_media DECIMAL(3, 1),
    popularidade DECIMAL(5, 2),
    FOREIGN KEY (id_filme) REFERENCES Dim_Filme(id_filme),
    FOREIGN KEY (id_genero) REFERENCES Dim_Genero(id_genero),
    FOREIGN KEY (id_decada) REFERENCES Dim_Decada(id_decada),
    FOREIGN KEY (id_pais) REFERENCES Dim_Pais(id_pais),
    FOREIGN KEY (id_plataforma) REFERENCES Dim_Plataforma(id_plataforma)
);