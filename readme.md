#  Temple Escape

**Temple Escape** é um jogo de aventura **point-and-click** com visão top-down, desenvolvido com **Python + PgZero**. O jogador deve coletar relíquias, evitar inimigos e escapar da caverna usando estratégia e stealth.

---

##  Objetivo do Jogo

Você está preso em uma caverna escura e precisa encontrar **3 relíquias antigas** para abrir a **porta de saída** e escapar.

Durante a jornada:

- **Inimigos patrulham** áreas e vão te perseguir se te virem.
- Você pode se **esconder em arbustos (bushes)** para evitar ser detectado.
- O jogo é controlado **apenas com o mouse**.

---

##  Como Jogar

| Ação                  | Como fazer                             |
|-----------------------|-----------------------------------------|
| **Mover o jogador**   | Clique com o mouse no destino desejado  |
| **Coletar relíquias** | Encoste na relíquia                     |
| **Esconder-se**       | Vá até um arbusto                       |
| **Evitar inimigos**   | Fuja do campo de visão ou esconda-se    |
| **Sair da caverna**   | Recolha 3 relíquias e vá até a porta    |

---

## 📋 Funcionalidades

-  Controle point-and-click (mouse)
-  Inimigos com IA de patrulha e perseguição
-  Sistema de stealth: arbustos para esconder
-  Porta de saída desbloqueável
-  Colisão com paredes
-  Animação de jogador e inimigos
-  Efeitos sonoros e música
-  HUD informativa
-  Sistema de menus (início, vitória, derrota)

---

##  Estrutura do Código

### `MAP_GRID`

- Mapa 2D definido por uma **grade de tiles 30x20**.
- Cada célula define o tipo de tile: parede, chão, arbusto, inimigo, relíquia, etc.
- Exemplo:

```python
MAP_GRID[6][8] = "R"  # Relíquia na posição (8,6)
MAP_GRID[4][6] = "E"  # Inimigo
MAP_GRID[9][2] = "P"  # Jogador
````

### `load_map()`

* Lê o `MAP_GRID` e instancia todos os objetos do jogo (parede, player, inimigos, etc).
* Garante que todos os tiles tenham um **chão (`ground`)**.

---

### Principais Classes

#### `Player`

* Responsável pelo movimento e animação do herói.
* Detecta colisão com arbustos, relíquias e inimigos.

#### `Enemy`

* Possui 2 modos: `patrol` (andar entre dois pontos) e `hunt` (perseguir jogador).
* Evita obstáculos como paredes e arbustos.
* Muda de direção ao colidir com parede ou ao chegar no fim da rota.

#### `Wall` e `Bush`

* Objetos com `Rect` (hitbox) para colisão.
* `Bush` permite que o player fique **invisível** aos inimigos.

#### `ExitDoor`

* Só é aberta quando 3 relíquias são coletadas.
* Leva o jogador à vitória.

#### `Relic`

* Coletável ao encostar com o jogador.

---

##  Assets

**Imagens esperadas (na pasta `/images`):**

* `wall.png` – parede
* `ground.png` – piso base
* `bush.png` – arbusto
* `relic.png` – relíquia
* `door.png`, `door_open.png` – porta
* `soldier_walk_00.png` até `soldier_walk_06.png`
* `soldier_idle_00.png` até `soldier_idle_04.png`
* `orc_walk_00.png` até `orc_walk_06.png`
* `orc_idle_00.png` até `orc_idle_04.png`

**Sons esperados (na pasta `/sounds`):**

* `pickup.ogg` – coletar relíquia
* `door.ogg` – abrir porta
* `hit.ogg` – ser pego por inimigo
* `hide.ogg` – entrar no arbusto

**Música (na pasta `/music`):**

* `bgm.ogg`

---

## 🚀 Requisitos para rodar

* Python 3.10+ (recomendado)
* PgZero instalado:

```bash
pip install pgzero
```

* Execute o jogo com:

```bash
pgzrun main.py
```

---

##  Estrutura do Projeto

```
TempleEscape/
├── main.py
├── images/
│   ├── wall.png
│   ├── ground.png
│   ├── relic.png
│   └── ... sprites ...
├── sounds/
│   ├── pickup.ogg
│   ├── hit.ogg
│   └── ...
├── music/
│   └── bgm.ogg
```

---

##  Progresso Atual

* [x] Sistema de mapas com grid
* [x] IA de patrulha e perseguição
* [x] Stealth via bushes
* [x] Portas e relíquias funcionais
* [x] Menu e HUD
* [ ] Sistema de save/load *(futuro)*
* [ ] Fases adicionais *(futuro)*

---

##  Créditos

Desenvolvido por: **Dilvonei Lacerda**

Tecnologia: [PgZero](https://pygame-zero.readthedocs.io)

---

```
