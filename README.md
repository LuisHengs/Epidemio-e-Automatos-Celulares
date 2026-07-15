## ▶️ Como Executar

Para iniciar a simulação, abra o terminal no diretório do projeto e execute o script principal:

```bash
python simulador_sir_similaridade.py
```

### 🎮 Controles Interativos da Simulação

Durante a execução da janela gráfica, você pode utilizar o teclado para interagir com o modelo:

* **`ESPAÇO`**: Pausa e retoma a evolução temporal (ideal para analisar a formação de clusters e frentes de onda).
* **`R`**: Reinicia a simulação com uma população totalmente suscetível e novos "pacientes zero" em locais aleatórios.
* **`ESC`**: Encerra o simulador.

---

## 🎨 Legenda de Cores (Estados Compartimentais)

A interface visual utiliza as seguintes cores para representar o estado de cada indivíduo (célula) na matriz:

* **Cinza Claro**: Suscetível (Indivíduo saudável, vulnerável ao contágio).
* **Vermelho**: Infectado (Indivíduo com o vírus ativo, propagando a doença para a vizinhança).
* **Azul**: Recuperado (Indivíduo curado que adquiriu imunidade, atuando como barreira espacial).

---

## ⚙️ Parâmetros Editáveis (Calibração do Modelo)

Para fins de experimentação acadêmica e geração de diferentes cenários epidemiológicos, você pode alterar os seguintes parâmetros diretamente no cabeçalho do código-fonte:

* `BETA`: Probabilidade de transmissão (contágio) por contato validado com um vizinho infectado.
* `GAMMA`: Probabilidade de recuperação espontânea (saída do compartimento I para o R).
* `I0`: Número inicial de infectados (pacientes zero) inseridos na matriz no tempo t=0.
* `GRID_SIZE`: Dimensão da matriz quadrada que representa a população (padrão: 120x120).

---

## 📚 Referências

* Albuquerque, J. (2016). *Computational Epidemiology*.
* Keeling, M. J., & Rohani, P. (2008). *Modeling Infectious Diseases in Humans and Animals*. Princeton University Press.
