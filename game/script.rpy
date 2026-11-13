################################################################################
##  PENSAMENTOS INTRUSIVOS
##  Um jogo de terror psicológico  |  Ren'Py 8.x
##
##  Este arquivo é o jogo inteiro:  game/script.rpy
##
##  ÍNDICE
##    1. PERSONAGENS
##    2. VARIÁVEIS
##    3. AJUSTES (tamanhos e sistema de impulso)
##    4. IMAGENS
##         4.1  Fundos (cenários)
##         4.2  Sprites da Mari       <- adicione/troque sprites AQUI
##         4.3  Sprites da Entidade   <- adicione/troque sprites AQUI
##         4.4  Outras imagens
##         4.5  Registro automático   (não precisa mexer)
##    5. EFEITOS DA MARI
##    6. EFEITOS DA ENTIDADE
##    7. SISTEMA DE IMPULSO (tempo, sussurros e botão que foge do mouse)
##    8. TELAS (HUD e título de local)
##    8b. MENU PRINCIPAL (a Entidade é o menu)
##    9. AUXILIARES
##   10. HISTÓRIA (aviso, início, cenas e finais)
##
##  PASTAS:
##    game/gui/bg/       -> fundos
##    game/gui/sprites/  -> Mari e Entidade
################################################################################


## ============================================================================
##  1. PERSONAGENS
## ============================================================================
define mari = Character("Mari", color="#f2c6d8")
define bia = Character("Bia", color="#9fd3ff")
define ent = Character("ELE", color="#ff2b3a", what_color="#ff8a93", what_italic=True, what_size=34, what_slow_cps=22)
define nar = Character(None, what_italic=True)


## ============================================================================
##  2. VARIÁVEIS
## ============================================================================
default calma = 3            # quanto ela consegue se ancorar no presente
default ruido = 0            # quanto a Entidade está alta na cabeça dela
default pediu_ajuda = False
default nomeou = False       # aprendeu a "dar nome" ao pensamento


## ============================================================================
##  3. AJUSTES  (mexa nestes números até ficar bom)
## ============================================================================
## Tamanhos
define mari_zoom = 1.0
define ent_zoom = 1.0           # tamanho normal da Entidade
define ent_zoom_perto = 1.15    # tamanho quando ela está "perto" (se cortar a cabeça, diminua)

## Menu de impulso
define impulso_tempo_base = 7.0    # segundos pra decidir com RUÍDO 0
define impulso_tempo_min = 3.5     # o tempo nunca fica menor que isso
define impulso_forca_base = 0.20   # quanto o botão é puxado pelo mouse (0 a 1)
define impulso_maximo = 140        # distância máxima que o botão anda, em pixels
define impulso_x = 960             # posição do botão da Entidade (centro da tela)
define impulso_y = 470


## ============================================================================
##  4. IMAGENS
## ============================================================================

## ----------------------------------------------------------------------------
##  4.1  FUNDOS (cenários)  |  pasta: game/gui/bg/
##  Usar na história:  scene bg nome
##  Para trocar um fundo, mude só o nome do arquivo.
## ----------------------------------------------------------------------------
image bg quarto_dia      = "gui/bg/quarto.png"
image bg quarto_noite    = "gui/bg/quarto_escuro.png"
image bg corredor        = "gui/bg/corredor.png"
image bg banheiro        = "gui/bg/banheiro.png"
image bg sala            = "gui/bg/sala.png"
image bg rua             = "gui/bg/rua.png"
image bg mercado         = "gui/bg/maquina.png"
image bg metro frente    = "gui/bg/metrolado.png"
image bg metro lado      = "gui/bg/metrofrente.png"  
image bg cozinha_noite   = "gui/bg/cozinha.png"


## ----------------------------------------------------------------------------
##  4.2  SPRITES DA MARI  |  pasta: game/gui/sprites/
##
##  COMO ADICIONAR UM SPRITE NOVO:
##    1. Salve o PNG em game/gui/sprites/   (ex.: mari_chorando.png)
##    2. Adicione UMA linha em SPRITES_MARI abaixo:   "chorando": "mari_chorando.png",
##    3. Use na história:                              show garota chorando
##
##  COMO TROCAR UM SPRITE:  mude só o nome do arquivo na linha dele.
##  Se o arquivo não existir, o jogo usa o sprite "neutra" no lugar (sem erro).
## ----------------------------------------------------------------------------
init python:

    ## nome usado no jogo  :  arquivo
    SPRITES_MARI = {
        # --- expressões ---
        "neutra":      "mari_neutra.png",      
        "falando":     "mari_falando.png",    
        "assustada":   "mari_assustada.png",    
        "assustada2":  "mari_assustada2.png",
        "olhosfechados": "mari_olhosfechados.png",
        "esquerda":    "mari_esquerda.png",
        "direita":     "mari_direita.png",
    }

    ## Apelidos: nomes alternativos que apontam pra um sprite acima.
    ## (Assim dá pra trocar qual sprite "medo" usa mudando UMA linha.)
    APELIDOS_MARI = {
        "normal": "neutra",       # usado como "padrão" em várias cenas
        "medo":   "assustada",    # usado quando a Entidade aparece
        "calma":  "neutra",       # usado nos finais bons
    }

    ## Qual sprite usar quando o arquivo de outro não existir:
    FALLBACK_MARI = "neutra"


## ----------------------------------------------------------------------------
##  4.3  SPRITES DA ENTIDADE  |  pasta: game/gui/sprites/
##
##  "_base" é o sprite principal:        show entidade
##  Para criar variações (ex.: sorrindo):
##    1. Salve em game/gui/sprites/      (ex.: entidade_sorrindo.png)
##    2. Adicione:  "sorrindo": "entidade_sorrindo.png",
##    3. Use:       show entidade sorrindo at ...
## ----------------------------------------------------------------------------
init python:

    SPRITES_ENTIDADE = {
        "_base":  "entidade.png",
        # "sorrindo": "entidade_sorrindo.png",
        # "perto":    "entidade_perto.png",
    }

    APELIDOS_ENTIDADE = {}

    FALLBACK_ENTIDADE = "_base"


## ----------------------------------------------------------------------------
##  4.4  OUTRAS IMAGENS
## ----------------------------------------------------------------------------
image preto = Solid("#000000")
image veu_vermelho = Transform(Solid("#7a0010"), alpha=0.0)


## ----------------------------------------------------------------------------
##  4.5  REGISTRO AUTOMÁTICO DOS SPRITES  (não precisa mexer aqui)
## ----------------------------------------------------------------------------
init 1 python:

    PASTA_SPRITES = "gui/sprites/"

    def _carregar_sprite(tag, arquivos, nome, fallback, zoom):
        caminho = PASTA_SPRITES + arquivos[nome]
        if not renpy.loadable(caminho):
            caminho = PASTA_SPRITES + arquivos[fallback]
        if not renpy.loadable(caminho):
            return Text("falta: " + caminho, color="#ff2b3a", size=24)
        return Transform(caminho, zoom=zoom)

    def registrar_sprites(tag, arquivos, apelidos, fallback, zoom=1.0):
        for nome in arquivos:
            img = tag if nome == "_base" else tag + " " + nome
            renpy.image(img, _carregar_sprite(tag, arquivos, nome, fallback, zoom))
        for apelido, destino in apelidos.items():
            img = tag + " " + apelido
            renpy.image(img, _carregar_sprite(tag, arquivos, destino, fallback, zoom))

    registrar_sprites("garota",   SPRITES_MARI,     APELIDOS_MARI,     FALLBACK_MARI,     zoom=mari_zoom)
    registrar_sprites("entidade", SPRITES_ENTIDADE, APELIDOS_ENTIDADE, FALLBACK_ENTIDADE)


## ============================================================================
##  5. EFEITOS DA MARI
## ============================================================================
## Respiração calma (base de quase todos os outros efeitos)
transform mari_respira:
    xalign 0.15 yalign 1.0
    block:
        ease 3.0 yoffset 5
        ease 3.0 yoffset 0
        repeat

## Entrada da cena
transform mari_entra:
    xalign 0.15 yalign 1.0 alpha 0.0 xoffset -40
    ease 0.8 alpha 1.0 xoffset 0
    mari_respira

## Susto: treme por um instante e depois se acalma
transform mari_susto:
    xalign 0.15 yalign 1.0
    block:
        linear 0.05 xoffset -4 yoffset 2
        linear 0.05 xoffset 4 yoffset 0
        repeat 12
    ease 0.3 xoffset 0 yoffset 0
    mari_respira

## Recua um pouco, sem tremer
transform mari_recua:
    xalign 0.15 yalign 1.0
    ease 0.6 xoffset -30
    mari_respira

## Tensa: respiração curta e acelerada, sem tremor
transform mari_tensa:
    xalign 0.15 yalign 1.0
    block:
        ease 1.2 yoffset 6
        ease 1.2 yoffset 0
        repeat

## Tremor contínuo (guardar para os momentos mais intensos)
transform mari_treme:
    xalign 0.15 yalign 1.0
    block:
        linear 0.06 xoffset -4 yoffset 2
        linear 0.06 xoffset 4 yoffset 0
        repeat


## ============================================================================
##  6. EFEITOS DA ENTIDADE
## ============================================================================
## Respirações (o "balanço" depois que ela já entrou)
transform entidade_respira:
    block:
        ease 2.5 zoom (ent_zoom * 1.04)
        ease 2.5 zoom ent_zoom
        repeat

transform entidade_respira_perto:
    block:
        ease 2.5 zoom (ent_zoom_perto * 1.03)
        ease 2.5 zoom ent_zoom_perto
        repeat

## Entrada 1: surge do nada, aumentando devagar
transform entidade_aparece:
    xalign 0.72 yalign 1.0 alpha 0.0 zoom (ent_zoom * 0.9)
    linear 1.4 alpha 1.0 zoom ent_zoom
    entidade_respira

## Entrada 2: desliza vindo da direita, de fora da tela
transform entidade_direita:
    xalign 0.72 yalign 1.0 zoom ent_zoom alpha 0.0 xoffset 900
    ease 1.6 alpha 1.0 xoffset 0
    entidade_respira

## Entrada 3: sobe devagar de baixo, ficando perto
transform entidade_sobe:
    xalign 0.72 yalign 1.0 zoom ent_zoom_perto alpha 0.0 yoffset 400
    ease 2.2 alpha 1.0 yoffset 0
    entidade_respira_perto

## Entrada 4: aparece atrás da Mari, espiando por cima do ombro
##            (usar com:  show entidade at entidade_atras behind garota)
transform entidade_atras:
    xalign 0.30 yalign 1.0 zoom ent_zoom alpha 0.0 yoffset 150
    linear 3.0 alpha 1.0 yoffset 0
    block:
        ease 3.5 xoffset 25
        ease 3.5 xoffset 0
        repeat

## Entrada 5: glitch, pisca e treme antes de se firmar
transform entidade_glitch:
    xalign 0.72 yalign 1.0 zoom ent_zoom alpha 0.0
    pause 0.3
    alpha 1.0
    pause 0.06
    alpha 0.0
    pause 0.08
    alpha 1.0 xoffset 14
    pause 0.05
    xoffset -14
    pause 0.05
    xoffset 0
    entidade_respira

## Piscar: some por um instante, de vez em quando (combinar com outra entrada)
transform piscar:
    alpha 1.0
    choice:
        pause 2.0
    choice:
        pause 4.0
    linear 0.04 alpha 0.0
    linear 0.04 alpha 1.0
    pause 0.1
    linear 0.04 alpha 0.0
    linear 0.04 alpha 1.0
    repeat

transform entidade_some:
    linear 1.5 alpha 0.0 zoom (ent_zoom * 0.5)

transform pulso_vermelho:
    alpha 0.0
    linear 0.15 alpha 0.55
    linear 1.2 alpha 0.0


## ============================================================================
##  7. SISTEMA DE IMPULSO
##  A opção da Entidade aparece grande e vermelha, treme e anda em direção ao
##  mouse, e a Entidade sussurra por cima. Se o tempo acabar, a escolha é dela.
##  Quanto maior o RUÍDO, mais rápido e mais forte fica.
##
##  COMO USAR NUMA CENA (em vez de "menu:"):
##    call screen escolha_impulso(impulso="opção da Entidade", saudaveis=["opção 0", "opção 1"], sussurros=["frase 1", "frase 2"])
##    if _return == 0:
##        (opção saudável 0)
##    elif _return == 1:
##        (opção saudável 1)
##    else:
##        (o jogador cedeu ao impulso, ou o tempo acabou)
##
##  Retorno (_return):  0, 1, 2...  = índice da opção saudável
##                      -1          = cedeu ao impulso (ou o tempo acabou)
## ============================================================================
init python:
    def atrair_mouse(bx, by, forca, maximo):
        estado = [0.0, 0.0]

        def _seguir(trans, st, at):
            mx, my = renpy.get_mouse_pos()
            alvo_x = max(-maximo, min(maximo, (mx - bx) * forca))
            alvo_y = max(-maximo, min(maximo, (my - by) * forca))
            estado[0] += (alvo_x - estado[0]) * 0.12
            estado[1] += (alvo_y - estado[1]) * 0.12
            trans.xoffset = estado[0] + renpy.random.uniform(-2, 2)
            trans.yoffset = estado[1] + renpy.random.uniform(-2, 2)
            return 0

        return _seguir

transform atrai(bx, by, forca, maximo):
    function atrair_mouse(bx, by, forca, maximo)

transform barra_tempo(t):
    xalign 0.5 ypos 1010 xzoom 1.0
    linear t xzoom 0.0

screen escolha_impulso(impulso, saudaveis, sussurros=None, tempo=None):
    modal True
    zorder 95

    default i = 0
    default falas = sussurros or ["faz.", "vai logo.", "você quer."]
    default posicoes = [0.25, 0.7, 0.45]
    default risco = max(0, ruido)
    default t = tempo or max(impulso_tempo_min, impulso_tempo_base - risco * 0.5)
    default forca = min(0.7, impulso_forca_base + risco * 0.06)

    ## A voz da Entidade, trocando de lugar e de frase
    text falas[i]:
        size 40
        italic True
        color "#ff2b3a"
        xalign posicoes[i % 3]
        ypos 200
        outlines [(2, "#000000", 0, 0)]
    timer 1.6 repeat True action SetScreenVariable("i", (i + 1) % len(falas))

    ## A opção da Entidade: grande, vermelha, fugindo do controle
    textbutton impulso:
        action Return(-1)
        xpos impulso_x
        ypos impulso_y
        xanchor 0.5
        yanchor 0.5
        xmaximum 900
        text_size 44
        text_color "#ff2b3a"
        text_hover_color "#ffffff"
        text_text_align 0.5
        text_outlines [(2, "#000000", 0, 0)]
        at atrai(impulso_x, impulso_y, forca, impulso_maximo)

    ## As opções saudáveis: pequenas e discretas
    vbox:
        xalign 0.5
        ypos 760
        spacing 14
        for n, texto in enumerate(saudaveis):
            textbutton texto:
                action Return(n)
                xalign 0.5
                text_size 24
                text_color "#8a8a99"
                text_hover_color "#8fe3c0"
                text_outlines [(1, "#000000", 0, 0)]

    ## Tempo acabando: a Entidade escolhe
    add Solid("#ff2b3a", xsize=700, ysize=6) at barra_tempo(t)
    timer t action Return(-1)


## ============================================================================
##  8. TELAS (HUD e título de local)
## ============================================================================
screen hud():
    zorder 100
    vbox:
        xpos 30
        ypos 30
        spacing 6
        text "RUÍDO" size 18 color "#ff2b3a" outlines [(1, "#000000", 0, 0)]
        bar value StaticValue(max(0, min(ruido, 8)), 8) xsize 220 ysize 14 left_bar Solid("#ff2b3a") right_bar Solid("#2a2a33")
        text "CALMA" size 18 color "#8fe3c0" outlines [(1, "#000000", 0, 0)]
        bar value StaticValue(max(0, min(calma, 8)), 8) xsize 220 ysize 14 left_bar Solid("#8fe3c0") right_bar Solid("#2a2a33")

screen titulo_local(nome):
    zorder 90
    text nome size 26 color "#ffffff" xalign 0.5 ypos 40 outlines [(2, "#000000", 0, 0)]
    timer 3.0 action Hide("titulo_local")


## ============================================================================
##  8b. MENU PRINCIPAL  (a Entidade é o menu)
##  Tela escura, a imagem da Entidade à direita (gui/sprites/entidade.png),
##  respirando, piscando e seguindo o mouse com um pequeno atraso.
##  Os botões ficam em fila, no lado esquerdo, e MUDAM DE FRASE quando o mouse
##  passa por cima. Frases esquisitas aparecem na tela, uma por vez, em lugares
##  diferentes a cada vez que o menu abre.
##
##  Se der erro de "screen main_menu already defined", apague o bloco
##  "screen main_menu():" que vem no arquivo screens.rpy do projeto.
## ============================================================================
init python:

    ## O que cada botão vira quando o mouse passa por cima (sorteia uma)
    FRASES_HOVER = {
        "jogar":     ["NÃO JOGA", "entra.", "Você vai amar isso."],
        "continuar": ["você voltou.", "Me salva...", "de onde parou?"],
        "opcoes":    ["mexer em mim?", "NÃO FODE COM MINHA MENTE", "Você é minha."],
        "sair":      ["vai fugir de novo?", "CORRE", "você vai voltar..."],
    }

    ## Frases que aparecem soltas na tela, uma por vez: (texto, tamanho, cor)
    FRASES_SOLTAS = [
        ("Deixa eu assumir",      66, "#ec0000"),
        ("ME DEIXA EM PAZ.", 50, "#fdfdfd"),
        ("eu lembro de você.",   44, "#fa0000"),
        ("CALA A BOCA!",           35, "#f6f6f8"),
        ("NÃO?",    44, "#f80000"),
        ("MARI.",  42, "#f7f7f8"),
        ("TEM ALGUÉM AI?",     52, "#f5f3f3"),
        ("você já esteve aqui.",       28, "#a8020a"),
        ("MARI...",     40, "#f80000"),
        ("NÃO. NÃO.",                   58, "#faf9f9"),
    ]

    ## Tempo que cada frase fica na tela (segundos). Não mexa sem ajustar a transform.
    TEMPO_FRASE = 5.0

    frase_menu = ""

    def sortear_frase(chave):
        global frase_menu
        frase_menu = renpy.random.choice(FRASES_HOVER[chave])

    ## Faz um objeto seguir o mouse com atraso
    def seguir_mouse(cx, cy, kx, ky, maxx, maxy, lag):
        est = [0.0, 0.0]

        def _f(trans, st, at):
            try:
                mx, my = renpy.get_mouse_pos()
            except Exception:
                mx, my = cx, cy
            alvo_x = max(-maxx, min(maxx, (mx - cx) * kx))
            alvo_y = max(-maxy, min(maxy, (my - cy) * ky))
            est[0] += (alvo_x - est[0]) * lag
            est[1] += (alvo_y - est[1]) * lag
            trans.xoffset = est[0]
            trans.yoffset = est[1]
            return 0

        return _f

## Ajustes do menu
define menu_ent_zoom = 1.0        # tamanho da Entidade no menu
define menu_ent_x = 0.70          # posição horizontal dela (0 = esquerda, 1 = direita)

## A Entidade no menu: aparece devagar, respira, pisca e segue o mouse
transform entidade_menu_t:
    xalign menu_ent_x
    yalign 1.0
    zoom menu_ent_zoom
    alpha 0.0
    linear 2.5 alpha 1.0
    parallel:
        function seguir_mouse(config.screen_width * menu_ent_x, 940, 0.42, 0.38, 320, 70, 0.76) #menu_ent_x, 740, 0.12, 0.08, 220, 50, 0.06)
    parallel:
        block:
            ease 3.0 zoom (menu_ent_zoom * 1.03)
            ease 3.0 zoom menu_ent_zoom
            repeat
    parallel:
        block:
            choice:
                pause 3.0
            choice:
                pause 6.0
            linear 0.05 alpha 0.15
            linear 0.05 alpha 1.0
            pause 0.12
            linear 0.04 alpha 0.3
            linear 0.04 alpha 1.0
            repeat

## Fundo vermelho que "bate" como um coração
transform batida:
    alpha 0.0
    block:
        linear 1.6 alpha 0.16
        linear 1.8 alpha 0.0
        pause 0.6
        repeat

## Mesmo fundo, mas acelerado (quando o mouse está em "sair")
transform batida_forte:
    alpha 0.0
    block:
        linear 0.35 alpha 0.38
        linear 0.45 alpha 0.05
        repeat

## Uma frase por vez: cada uma espera a sua vez, aparece, treme (glitch),
## sobe um pouquinho e some. vez = posição na fila | n = total de frases
transform aparece_um(vez, n):
    alpha 0.0
    pause (vez * 5.0)
    block:
        parallel:
            linear 1.0 alpha 0.55
            pause 2.5
            linear 0.04 alpha 0.1
            linear 0.04 alpha 0.55
            pause 0.4
            linear 1.0 alpha 0.0
        parallel:
            yoffset 0
            linear 5.0 yoffset -24
        pause ((n - 1) * 5.0)
        repeat


screen main_menu():
    tag menu
    default hov = ""

    ## A ordem e os lugares das frases mudam toda vez que o menu abre
    default ordem = renpy.random.sample(list(range(len(FRASES_SOLTAS))), len(FRASES_SOLTAS))
    default posicoes = [(renpy.random.randint(520, 1200), renpy.random.randint(110, 940)) for _ in range(len(FRASES_SOLTAS))]

    add Solid("#030305")
    add Solid("#6a0010") at (batida_forte if hov == "sair" else batida)

    ## ---- Frases esquisitas, uma por vez, em lugares diferentes ----
    for k, idx in enumerate(ordem):
        $ txt, tam, cor = FRASES_SOLTAS[idx]
        text txt size tam italic True color cor xpos posicoes[k][0] ypos posicoes[k][1] at aparece_um(k, len(ordem))

    ## ---- A Entidade ----
    add "entidade" at entidade_menu_t

    ## ---- Botões em fila, no lado esquerdo ----
    vbox:
        xpos 90
        yalign 0.55
        spacing 30

        textbutton (frase_menu if hov == "jogar" else "jogar"):
            action Start()
            hovered [SetScreenVariable("hov", "jogar"), Function(sortear_frase, "jogar")]
            unhovered SetScreenVariable("hov", "")
            xminimum 560
            text_size 52
            text_italic True
            text_color "#8a8a99"
            text_hover_color "#ff2b3a"
            text_outlines [(2, "#000000", 0, 0)]

        textbutton (frase_menu if hov == "continuar" else "continuar"):
            action ShowMenu("load")
            hovered [SetScreenVariable("hov", "continuar"), Function(sortear_frase, "continuar")]
            unhovered SetScreenVariable("hov", "")
            xminimum 560
            text_size 52
            text_italic True
            text_color "#8a8a99"
            text_hover_color "#ff2b3a"
            text_outlines [(2, "#000000", 0, 0)]

        textbutton (frase_menu if hov == "opcoes" else "opções"):
            action ShowMenu("preferences")
            hovered [SetScreenVariable("hov", "opcoes"), Function(sortear_frase, "opcoes")]
            unhovered SetScreenVariable("hov", "")
            xminimum 560
            text_size 52
            text_italic True
            text_color "#8a8a99"
            text_hover_color "#ff2b3a"
            text_outlines [(2, "#000000", 0, 0)]

        textbutton (frase_menu if hov == "sair" else "sair"):
            action Quit(confirm=True)
            hovered [SetScreenVariable("hov", "sair"), Function(sortear_frase, "sair")]
            unhovered SetScreenVariable("hov", "")
            xminimum 560
            text_size 52
            text_italic True
            text_color "#8a8a99"
            text_hover_color "#ff2b3a"
            text_outlines [(2, "#000000", 0, 0)]


## ============================================================================
##  9. AUXILIARES
## ============================================================================
## Fim de cada cena: a Entidade some e a Mari volta a respirar
label acalmar:
    show garota normal at mari_respira
    hide entidade
    return


## ============================================================================
##  10. HISTÓRIA
## ============================================================================

## ----------------------------------------------------------------------------
##  AVISO DE CONTEÚDO
## ----------------------------------------------------------------------------
label splashscreen:
    scene preto
    with Pause(0.5)
    show text "{size=34}{color=#ff2b3a}AVISO DE CONTEÚDO{/color}{/size}\n\n{size=24}Este jogo aborda ansiedade, TOC e pensamentos intrusivos,\nincluindo pensamentos sobre se machucar (sem mostrar atos).\n\nPensamento intrusivo não é vontade. É o cérebro disparando um alarme falso.\n\nSe você está mal de verdade, converse com alguém.\nNo Brasil, o CVV atende 24h, de graça, pelo {b}188{/b}.{/size}" at truecenter
    with dissolve
    pause 7.0
    hide text
    with dissolve
    return


## ----------------------------------------------------------------------------
##  INÍCIO
## ----------------------------------------------------------------------------
label start:
    scene preto
    show text "{size=60}{color=#ffffff}PENSAMENTOS\nINTRUSIVOS{/color}{/size}" at truecenter
    with dissolve
    pause 2.5
    hide text
    with dissolve
    show screen hud
    jump cena_quarto


## ============================================================================
##  CENA 1 – QUARTO (MANHÃ)
##  Entidade: atrás da Mari, no reflexo  |  Mari: treme só no susto
##  Escolha: MENU DE IMPULSO (o impulso é a compulsão de checar a porta)
## ============================================================================
label cena_quarto:
    scene bg quarto_dia
    with fade
    show screen titulo_local("Quarto – 7h12")
    show garota neutra at mari_entra
## barulho de despertador
    nar "O despertador toca pela terceira vez."
    nar "Mari se levanta. O dia ainda nem começou e a cabeça dela já está cheia."
    show garota falando
    mari "Só levantar. É só levantar."
    show garota olhosfechados
    mari "..."

    show garota neutra
    mari "preciso tomar café pra ir ao trabalho..."
    mari "meu dia vai ser longo."
    mari "melhor eu me apressar..."

    show garota medo at mari_susto
    show entidade at entidade_atras behind garota
    # play sound "audio/sussurro.ogg"   # descomente se tiver o arquivo
    ent "Mari"
    ent "Marizinha..."
    ent "pra que tanta pressa?"
    show garota direita
    mari "Não... você de novo não..."
    ent "Por que você não volta a dormir?"
    ent "faltar um dia de trabalho não vai causar tantos problemas assim..."

    call screen escolha_impulso(impulso="Ignorar o pensamento.", saudaveis=["Respirar fundo e ir tomar banho.", "Discutir com ele."], sussurros=["a porta.", "MARI!", "vai dormir!", "Tira essa roupa...", "MARI!", "MARI..."])

    if _return == 0:
        $ calma += 2
        $ ruido -= 1
        mari "melhor eu ir tomar um banho, ou vou me atrasar."
        mari "talvez um banho refrescante me ajude a esquecer tudo isso."
        mari "sim, vai dar certo."
        mari "hahaha, vai dar certo sim!"
        ent "Você é louca..."
        ent "Eu amo isso."
        ent "Eu vou te dominar, você não resiste em me ter por perto..."

    elif _return == 1:
        $ ruido += 2
        mari "Cala a boca! Cala a boca sua doença maldita! Eu não sou assim!"
        ent "Então por que você está me respondendo?"
        mari "E-eu..."
        show veu_vermelho at pulso_vermelho
        with hpunch
        ent "07:40"
        ent "Alguém vai se atrasar pro trabalho."
        ent "tic..."
        ent "tac..."
        ent "tic..."
        ent "tac..."
        mari "Ahn!!??"
        with hpunch
        mari "NÃO ACREDITO QUE PERDI MEU TEMPO FALANDO COM VOCÊ."
        ent "Falando com você mesma."
        ent "Eu existo? sim."
        nar "Parece que ele tem razão."
        nar "Você corre pro banheiro, liga o chuveiro e começa a tomar seu banho."
        nar "07:55"
        nar "Você vai pro trabalho sem comer nada..."
        nar "Denovo."

    else:
        $ ruido += 1
        nar "Ela desiste de tentar falar algo."
        nar "A dúvida nunca fica satisfeita. ela olha pra cama."
        mari "talvez se..."
        mari "..."
        mari "NÃO."
        mari "Isso e só uma desculpa idiota..."
        mari "preciso ir pro trabalho, agora mesmo."
        mari "Não fode com minha cabeça seu maldito!"
        ent "Eu? olhe pra você mesma."
        ent "quem é o louco aqui?"
        mari "..."
        nar "Acho que ele tem razão..."
    call acalmar
    jump cena_rua


## ============================================================================
##  CENA 2 – RUA (FAIXA DE PEDESTRES)
##  Entidade: desliza vindo da direita, piscando  |  Mari: recua, sem tremer
##  Escolha: MENU CLÁSSICO (pra variar o ritmo)
## ============================================================================
label cena_rua:
    scene bg rua
    with fade
    show screen titulo_local("Avenida – 8h05")
    show garota normal at mari_entra

    nar "Ônibus, buzinas, gente com pressa. Mari espera o sinal fechar."
    nar "Os carros passam a centímetros da calçada."

    show garota medo at mari_recua
    show entidade at entidade_direita, piscar
    ent "E se você desse um passo?"
    ent "Esses carros iam destroçar seus ossos em instantes..."
    nar "O coração dela dispara. As mãos suam."
    mari "Isso é excitante..."
    with hpunch
    mari "QUE!?"
    mari "NÃO, NÃO HAHAHAH ISSO É LOUCURA."
    mari "FOI VOCÊ, NÃO EU..."
    ent "Eu?"
    ent "E quem foi que cogitou isso?"
    mari "N-não... eu não disse nada."
    ent "Tem certeza?..."
    show veu_vermelho at pulso_vermelho
    with vpunch

    nar "Ela não moveu um músculo. E mesmo assim sente culpa, so pelo fato de ter pensado isso..."

    menu:

        "Segurar firme no poste e dar um passo pra trás, longe da beirada.":
            $ calma += 1
            $ ruido -= 1
            $ nomeou = True
            nar "Ela cola as costas no muro. Longe do meio-fio."
            mari "É um pensamento. Não é um plano. Não é um desejo."
            ent "..."
            nar "Pela primeira vez, ele hesita."

        "Eu quero isso?":
            $ calma += 1
            $ nomeou = True
            mari "Não. Eu quero chegar no trabalho. Quero pizza hoje à noite."
            mari "Quero ver o final daquela série."
            ent "Então por que eu existo?"
            mari "NÃO SEI. MAS VOCÊ NÃO FAZ PARTE DE MIM!"
            ent "Eu sou você, Mari."
            ent "Sou a parte que você deve aceitar."

        "Fechar os olhos e tapar os ouvidos até abrir o sinal.":
            $ ruido += 1
            nar "No escuro, ele fica mais alto. Ela só ouve a própria respiração."
            ent "Não adianta fechar os olhos. Eu estou aqui dentro."
            nar "Alguém esbarra nela. O sinal abriu."
            mari "huff..."
            mari "V-viu... é so uns pensamentos estranhos."

            ##quebra da quarta parede kkkk
            ##entidade olha pra tela e se aproxima fechando tudo e puçando pro supermercado
            ##ent "Não é nao."
    call acalmar
    jump cena_mercado


## ============================================================================
##  CENA 3 – SUPERMERCADO
##  Entidade: glitch, aparece piscando  |  Mari: tensa, sem tremer
##  Mari olha pros dois lados e depois pra frente (esquerda > direita > assustada2)
##  Escolha: MENU DE IMPULSO (o impulso é esconder e dizer que está tudo bem)
## ============================================================================
label cena_mercado:
    scene bg mercado
    with fade
    show screen titulo_local("Supermercado – 18h40")
    show garota normal at mari_entra

    nar "As luzes brancas zumbem. Corredores demais, gente demais."
    nar "O celular vibra. É a Bia."
    ent "Desliga."
    
    menu:

        "Atender.":

            bia "Oi, Mari!"
            mari "\"É a Bia... não falo com ela faz uma semana.\""
            bia "Mari! Vai no aniversário do Léo sábado? Tá tão sumida..."
            show garota falando
            mari "Ah... vou sim. Talvez."
            mari "Você sabe que dia vao ser-"

            show garota direita at mari_tensa
            show entidade at entidade_glitch
            ent "Ela nem quer você lá."
            ent "Você é estranha..."
            ent "Todo mundo aqui sabe disso."
            ent "O jeito esquisito que você anda, seu jeito de falar... eles percebem."
            ent "Toda desengonçada."

            ## --- Mari olha em volta: um lado, o outro, e depois pra frente ---
            show garota esquerda with Dissolve(0.15)
            ent "Olha como a mulher do caixa de olha feio."
            ent "Ela deve estar te xingando de piranha agora..."
            show garota direita with Dissolve(0.15)
            ent "E o velho comprando pão."
            ent "Ele está secando sua bunda faz 12 minutos."
            show garota assustada2 with Dissolve(0.15)
            ent "Ou aquele homem ali-"
            bia "Alô? Mari?"
            mari "CALA A BOCA!"
            bia "O QUE?"
            bia "O QUE DEU EM VOCÊ, MARI?"
            mari "NÃO... DESCULPA, NÃO FALEI PRA VOCÊ..."
            mari "BIA??"
            bia "Olha, mari... não sei o que está acontecendo com você."
            bia "Talvez você devesse..."
            bia "Procurar ajuda médica ou de um psicológo."
            mari "hm?? o que?..."
            mari "Acha que estou ficando louca?"
            mari "EU NÃO ESTOU."
            mari "EU NÃO PRECISO DA DROGA DE PSICOLÓGO NENHUM."
            bia "Calma, Mari... eu so quero ajud-"
            mari "A CULPA E DELE!"
            mari "A CULPA E DESSE MALDITO QUE NÃO SAI DA MINHA CABEÇA."
            mari "ELE NÃO ME DEIXA EM PAZ..."
            bia "..."
            bia "Mari..."
            bia "Eu sei que você ficou bem abalada depois que você terminou com o Léo."
            bia "Mas não precisa ficar desse jeito."
            bia "Você tem que superar ele..."
            mari "O QUE?..."
            mari "VOCÊ ACHA QUE ISSO TUDO E POR CAUSA DE UM EX RELACIONAMENTO DE MERDA?"
            mari "VAI SE FUD&ER SUA PIR@NHA DE MERDA..."
            mari "VOCÊS NUNCA LIGARAM PRA MIM..."
            mari "SO SE IMPORTAM COM O PRÓPRIO RABO."
            mari "E TEM MAIS SUA V@DIA-"
            nar "piiiiiiiiiiiiiiii........."
            nar "Bia desligou bem na sua cara."
            ent "Eu falei..."
            ent "Eles nunca foram seus amigos."
            ent "Que tipo de amigo não entende o outro ne?"
            ent "Ela é patetica..."
            ent "Você não vê?"
            ent "Eu me importo com você, Mari."
            ent "Eu so quero o... seu bem..."

        "Desligar.":
            show garota olhosfechados
            mari "Sua sanidade ja não está boa o suficiente pra abrir a boca agora."
            nar "Você desliga o telefone, Bia pode esperar."
            show veu_vermelho at pulso_vermelho

    call acalmar
    jump cena_cozinha


## ============================================================================
##  CENA 4 – COZINHA (NOITE)
##  Entidade: sobe de baixo, perto  |  Mari: tremor contínuo (pico de tensão)
##  Escolha: MENU DE IMPULSO (o impulso é ficar encarando a faca)
## ============================================================================
label cena_cozinha:
    scene bg cozinha_noite
    with fade
    show screen titulo_local("Cozinha – 22h17")
    show garota normal at mari_entra

    mari "Ahnn... finalmente cheguei em casa."
    nar "Mari corta um pedaço de pão. A faca brilha sob a luz fraca do{w=0.4}{nw}"
    nar "A panela ainda quente no fogão."

    show garota medo at mari_treme
    show entidade at entidade_sobe
    ent "Está cansada, Mari?..."
    ent "Eu tenho uma solução."
    ent "Olha a faca."
    ent "E se você acabasse com seus problemas agora?"
    mari "C-COMO ASSIM?..."
    nar "Ela sente o estômago revirar."
    mari "Para. Para, por favor."
    ent "Você poderia tentar. Só pra provar que consegue controlar."
    ent "Ou pra provar que não consegue."
    show veu_vermelho at pulso_vermelho
    with hpunch

    menu:

        "pegar a faca":
            nar "Ela pega a faca com a mão, mas nao sabe o motivo."
            nar "As mãos dela tremem. Mas em nenhum momento ela quis isso."
            nar "O pensamento é ruidoso. A vontade dela, não."
            ent "vai..."
            ent "Você consegue, Mari..."
            ent "Eu confio em você."
            mari "E-eu...."
            mari "Eu consigo, ne?"
            mari "Então é isso que vou fazer."
            mari "Por que eu consigo, ne??..."
            mari "EU CONSIGO HAHAHA..."
            mari "Eu... ham..."
            with hpunch
            mari "NÃO.. O QUE EU TO FAZENDO."
            nar "Mari larga a faca."
            nar "Ela cai no chão."
    call acalmar
    jump cena_final


## ============================================================================
##  CENA 5 – QUARTO (NOITE) / CONFRONTO
##  Entidade: atrás da Mari de novo, piscando  |  Mari: treme só no susto
## ============================================================================
label cena_final:
    scene bg quarto_noite
    with fade
    show screen titulo_local("Quarto – 3h03")
    show garota normal at mari_entra

    nar "Ela não consegue dormir. O teto parece mais baixo."
    nar "Mari sente sua cabela pesada..."
    nar "Ela se levanta da cama para ir na cozinha tomar um gole de água."

    show garota medo at mari_susto
    mari "Uahhhh.... que dor..."
    mari "hmnh... que horas são agora..."

    show entidade at entidade_atras, piscar behind garota
    ent "03:08 da manhã querida."
    with hpunch
    mari "AHHHHHHHHHHHHHHHHHHHH"

    ent "Eu sou tão horrivel assim?"
    mari "VOCÊ ME ASSUSTOU!"
    ent "Mari... Mari... Mari..."
    ent "Volte a dormir Mari..."
    ent "Você está com insonia pequena Mari."
    ent "Isso me lembra quando você era criança."
    ent ""


    if ruido >= 5:
        jump final_ruim
    elif calma >= 8 and pediu_ajuda:
        jump final_bom
    else:
        jump final_neutro


## ----------------------------------------------------------------------------
##  FINAL BOM – "Eu ouço você. Mas não te obedeço."
## ----------------------------------------------------------------------------
label final_bom:
    mari "Não. Você não é eu."
    mari "Você é o medo que eu tenho de mim mesma. É só isso."
    ent "..."
    mari "Eu ouço você. Mas não sou obrigada a te obedecer."
    mari "E amanhã, eu vou pedir ajuda de verdade."

    show entidade at entidade_some
    with hpunch
    show garota calma at mari_respira
    nar "Ele não morre. Ele encolhe."
    nar "Vira um sussurro no canto do quarto. Um ruído de fundo."
    nar "Ainda vai voltar, talvez. Mas agora Mari sabe o que ele é."

    scene bg quarto_dia
    show garota calma at mari_entra
    with fade
    nar "Manhã seguinte. Ela marca uma consulta com um psicólogo."
    nar "As mãos ainda tremem um pouco, mas dessa vez ela sabe que não está sozinha."

    show text "{size=40}FINAL: {color=#8fe3c0}O RUÍDO DE FUNDO{/color}{/size}" at truecenter
    with dissolve
    pause 3.0
    jump creditos


## ----------------------------------------------------------------------------
##  FINAL NEUTRO – "Por enquanto, ela aguenta."
## ----------------------------------------------------------------------------
label final_neutro:
    mari "Eu não sei o que você é."
    mari "Só sei que eu não quero te obedecer."
    ent "Isso não me impede de voltar."
    mari "Eu sei."

    show garota normal at mari_respira
    show entidade at entidade_some
    nar "Ele some devagar. Mari fica acordada até o céu clarear."
    nar "Ela sobreviveu a mais uma noite, mas sabe que sozinha não vai dar."
    nar "Da próxima vez, talvez ela conte pra alguém."

    show text "{size=40}FINAL: {color=#ffd27f}AMANHECER CANSADO{/color}{/size}" at truecenter
    with dissolve
    pause 3.0
    jump creditos


## ----------------------------------------------------------------------------
##  FINAL RUIM – "O silêncio também é uma prisão."
## ----------------------------------------------------------------------------
label final_ruim:
    show veu_vermelho at pulso_vermelho
    with vpunch
    ent "Todos esses dias, Mari. Todos esses dias e você não contou pra ninguém."
    ent "Porque você sabe que eles também iam achar que você é louca."
    mari "Eu não sou... eu não sou..."
    nar "Ela puxa o cobertor até a cabeça. A voz dele não diminui."
    nar "Mari não fez nada do que ele disse. Nunca fez."
    nar "Mas a culpa por ter pensado pesa como se tivesse feito."

    hide entidade
    scene preto
    with fade
    nar "O pensamento intrusivo se alimenta do segredo."
    nar "Quanto mais escondido, mais forte ele fica."
    nar "Falar sobre ele, com alguém de confiança ou com um profissional, tira o poder dele."

    show text "{size=40}FINAL: {color=#ff2b3a}O SEGREDO{/color}{/size}" at truecenter
    with dissolve
    pause 3.0
    jump creditos


## ============================================================================
##  CRÉDITOS / MENSAGEM FINAL
## ============================================================================
label creditos:
    hide screen hud
    scene preto
    with fade
    show text "{size=32}{color=#ffffff}PENSAMENTOS INTRUSIVOS{/color}{/size}\n\n{size=22}Ter pensamentos assustadores não faz de você uma pessoa má,\nperigosa ou louca.\nÉ um sintoma comum de ansiedade e TOC, e tem tratamento.\n\nSe você precisa conversar, ligue para o {b}CVV: 188{/b}\n(24h, gratuito, todo o Brasil)\nou procure um psicólogo ou psiquiatra.\n\n{i}Obrigado por jogar.{/i}{/size}" at truecenter
    with dissolve
    pause
    return
