###
###  Gabarit pour l'application de traitement des frequences de mots dans les oeuvres d'auteurs divers
###  Le traitement des arguments a ete inclus:
###     Tous les arguments requis sont presents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  Frederic Mailhot, 26 fevrier 2018
###    Revise 16 avril 2018
###    Revise 7 janvier 2020

###  Parametres utilises, leur fonction et code a generer
###
###  -d   Deja traite dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le repertoire d'auteurs
###       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
###
###  -P   Si utilise, indique au systeme d'utiliser la ponctuation.  Ce qui est considére comme un signe de ponctuation
###       est defini dans la liste PONC
###       Si -P EST utilise, cela indique qu'on désire conserver la ponctuation (chaque signe est alors considere
###       comme un mot.  Par defaut, la ponctuation devrait etre retiree
###
###  -m   mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
###
###  -a   Auteur (unique a traiter).  Utile en combinaison avec -g, -G, pour la generation d'un texte aleatoire
###       avec les caracteristiques de l'auteur indique
###
###  -G   Indique qu'on veut generer un texte (voir -a ci-haut), le nombre de mots à generer doit être indique
###
###  -g   Indique qu'on veut generer un texte (voir -a ci-haut), le nom du fichier en sortie est indique
###
###  -F   Indique qu'on desire connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
###       donné avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
###
###  -v   Deja traite dans le gabarit:  mode 'verbose',  va imprimer les valeurs données en parametre
###
###
###  Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
###  des autres parametres, le systeme produira differentes sorties:
###
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  'auteur:  mot  frequence'
###                la frequence doit être un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  'nom du fichier: auteur'
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramètres (fait deja partie du gabarit)

import math
import argparse
import glob
import sys
import os
import re
import random

from pathlib import Path
from collections import deque # Liste chainée
from operator import itemgetter

### Ajouter ici les signes de ponctuation à retirer
PONC = ['!', ')', '(', ',', '.', ';', ':', '?', '-', '_', '—']
SPACE = ['\t', '\n', '\r']

class Markov:
    def __init__(self, order):
        self.order = order
        self.chain = {}
        self.word_stats = {}
        self.key_stats = {}
        self.word_pattern = re.compile('^[a-z\u00e0-\u00f60-9]{3,}$')

    def add_or_insert(self, table, key, elem):
        if key in table:
            table[key] += elem
        else:
            table[key] = elem

    def add_word(self, key, word):
        # Compte les clés
        self.add_or_insert(self.key_stats, key, 1)
        # Compte les mots
        self.add_or_insert(self.word_stats, word, 1)
        # Ajouter à la chaine
        self.add_or_insert(self.chain, key, [word])

    def most_frequent(self, n):
        if n <= 0 or n > len(self.word_stats):
            print('La position passée par -F ({}) est hors du tableau.'
                    .format(n));
            return '', 0

        sorted_words = sorted(self.word_stats.items(),
                key = itemgetter(1), reverse = True)
        return sorted_words[n - 1]

    def analyze(self, words):
        buf = deque()
        key = ''

        for word in words:
            self.add_word(key, word)

            # Actualise la liste
            buf.append(word)
            while len(buf) > self.order:
                buf.popleft()

            # Reconstruit la clé
            key = ''
            for item in buf:
                key += item;

        # Ajouter le dernier mot
        self.add_word(key, word)

    def vomit(self, word_count):
        buf = deque()
        key = ''
        text = ''

        random.seed()
        for i in range(word_count):
            # Choisit un mot au hasard selon la clé
            if key in self.chain:
                word = random.choice(self.chain[key])
            else:
                # On fait simplement arrêter si on ne peut plus avancer
                break

            # Actualise la liste
            buf.append(word)
            while len(buf) > self.order:
                buf.popleft()

            # Reconstruit la clé
            key = ''
            for item in buf:
                key += item;

            # Ajoute le mot au texte
            text += word + ' '

        return text.rstrip()

    def generate_words(self, text, space_equiv):
        data = text.lower()
        # Remplace le contenu de space_equiv par des espaces
        for item in space_equiv:
            data = data.replace(item, ' ')

        # Sépare le texte par espace
        raw_words = data.split(' ')

        # Ajoute les mots valides dans words
        words = deque()
        for word in raw_words:
            if self.is_valid_word(word):
                words.append(word)
            elif len(word) > 2:
                print("Possible error case: {}".format(word))

        return words

    def is_valid_word(self, word):
        return len(word) > 2
        # return self.word_pattern.search(word) is not None

    # Compare two frequency graphs implemented as dictionaries
    def compare(self, d1, d2):
        ours = d1.keys()
        theirs = d2.keys()
        common = []
        magic = 0

        # Assume their chain is smaller
        for elem in theirs:
            if elem in ours:
                common.append(elem)

        for elem in common:
            our_freq = d1[elem]/len(common)
            their_freq = d2[elem]/len(common)
            magic += (our_freq + their_freq)**2

        return math.sqrt(magic)

    def compare_words(self, other):
        return self.compare(self.key_stats, other.key_stats)

    def compare_ngrams(self, other):
        return self.compare(self.word_stats, other.word_stats)

def read_author(directory, author):
    paths = glob.glob('{}/{}/*.txt'.format(directory, author))
    texts = deque()

    for path in paths:
        with open(path, 'r') as f:
            texts.append(f.read())

    return texts

### Main: lecture des paramètres et appel des méthodes appropriées
###
###       argparse permet de lire les paramètres sur la ligne de commande
###             Certains paramètres sont obligatoires ('required=True')
###             Ces paramètres doivent êtres fournis à python lorsque l'application est exécutée
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='markov_ciml3101.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-A', action='store_true', help='Traiter tous les auteurs')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', default=2, type=int, help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer (on part de 1)')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    # parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    args = parser.parse_args()

    ### Lecture du répertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des répertoires d'auteurs, peu importe le système d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)

    ### Enlever les signes de ponctuation (ou non) - Définis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    if args.v:
        print('Mode verbose:')
        print('Calcul avec les auteurs du repertoire: ' + args.d)
        if args.f:
            print('Fichier inconnu a,'
                  ' etudier: ' + args.f)

        print('Calcul avec des ' + str(args.m) + '-grammes')
        if args.F:
            print(str(args.F) + 'e mot (ou digramme) le plus frequent sera calcule')

        if args.a:
            print('Auteur etudie: ' + args.a)

        if args.P:
            print('Retirer les signes de ponctuation suivants: {0}'.format(' '.join(str(i) for i in PONC)))

        if args.G:
            print('Generation d\'un texte de ' + str(args.G) + ' mots')

        # if args.g:
            # print('Nom de base du fichier de texte genere: ' + args.g)

        print('Repertoire des auteurs: ' + rep_aut)
        print('Liste des auteurs: ')
        for a in authors:
            aut = a.split('/')
            print('    ' + aut[-1])

        print('')

        space_equiv = SPACE
        if remove_ponc:
            space_equiv += PONC

        chains = {}
        if args.A:
            for author in authors:
                chains[author] = Markov(args.m)
        elif args.a in authors:
            chains[args.a] = Markov(args.m)
        else:
            print('Soit un auteur valide dans -a ou -A est requis.')
            sys.exit(1)

        for (author, chain) in chains.items():
            texts = read_author(rep_aut, author)
            for text in texts:
                # Slip it to the android
                words = chain.generate_words(text, space_equiv)
                chain.analyze(words)

        if args.G:
            for (author, chain) in chains.items():
                # Slip it to the android
                vomit = chain.vomit(args.G)
                print('Texte généré pour {}:\n :: Début:\n\t{}\n :: Fin\n'
                        .format(author, vomit))

        print('')

        if args.F:
            for (author, chain) in chains.items():
                word, count = chain.most_frequent(args.F)
                print('Position {} par fréquence pour {}: {} (répété {} fois)'
                        .format(args.F, author, word, count))

        print('')

        if args.f:
            with open(args.f) as f:
                validation_chain = Markov(args.m)
                text = f.read()

            words = validation_chain.generate_words(text, space_equiv)
            validation_chain.analyze(words)

            print('Comparaison avec {}:'.format(args.f))
            for (author, chain) in chains.items():
                magic = chain.compare_ngrams(validation_chain)
                print('{}: {}'.format(author, magic))
