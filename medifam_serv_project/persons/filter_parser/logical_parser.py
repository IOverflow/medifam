from enum import IntEnum
import re
from typing import List, Tuple
from functools import singledispatch

from django.db.models.query_utils import Q


class ParsingException(Exception):
    pass


# Ast
class Node:
    pass


class NotNode(Node):
    def __init__(self, expr: Node) -> None:
        self.expr = expr


class OrNode(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right


class AndNode(Node):
    def __init__(self, left: Node, right: Node) -> None:
        self.left = left
        self.right = right


class Operand(Node):
    def __init__(self, value: str) -> None:
        self.value = value


# We don't need a complicated LL(1) parser implementation.
# Just a simple predictive-recursive parser, no precedence level
# or something like that. (Pffff)

# Tokenizer is also simple enough, just a couple regex and a one pass through
# the text
class TokenType(IntEnum):
    OR = 0
    AND = 1
    LEFT_PAREN = 2
    RIGHT_PAREN = 3
    OPERAND = 4
    SPACE = 5
    NOT = 6


class Token:
    def __init__(self, lex: str, tt: TokenType) -> None:
        self.lex = lex
        self.tt = tt


TOKENS = [
    (re.compile(r"\|"), TokenType.OR),
    (re.compile(r"\&&"), TokenType.AND),
    (re.compile(r"\("), TokenType.LEFT_PAREN),
    (re.compile(r"\)"), TokenType.RIGHT_PAREN),
    (re.compile(r"\-"), TokenType.NOT),
    (re.compile(r"\s+"), TokenType.SPACE),
    (re.compile(r"\w+"), TokenType.OPERAND),
]


def tokenize(text: str):
    tokens = []
    while text:
        for token, token_type in TOKENS:
            match = token.match(text)
            if match:
                text = text[match.end() :]
                if token_type != TokenType.SPACE:
                    tokens.append(Token(match.group(), token_type))
    return tokens


def parse_expr(tokens: List[Token]) -> Tuple[Node, List[Token]]:
    expr, tokens = parse_operand(tokens)
    if tokens:
        if tokens[0].tt == TokenType.AND:
            right, toks = parse_expr(tokens[1:])
            return AndNode(expr, right), toks
        elif tokens[0].tt == TokenType.OR:
            right, toks = parse_expr(tokens[1:])
            return OrNode(expr, right), toks
    return expr, tokens


def parse_operand(tokens: List[Token]) -> Tuple[Node, List[Token]]:
    if tokens[0].tt == TokenType.LEFT_PAREN:
        expr, tokens = parse_expr(tokens[1:])
        if not tokens[0].tt == TokenType.RIGHT_PAREN:
            raise ParsingException()
        return expr, tokens[1:]
    
    elif tokens[0].tt == TokenType.NOT:
        expr, tokens = parse_expr(tokens[1:])
        return NotNode(expr), tokens

    return Operand(tokens[0].lex), tokens[1:]


def parse(text: str) -> Node:
    expr, tokens = parse_expr(tokenize(text))
    if tokens:
        raise ParsingException()
    return expr


@singledispatch
def evaluate(node: Node, name: str):
    return Q()


@evaluate.register
def _(node: AndNode, name: str):
    left = evaluate(node.left, name)
    right = evaluate(node.right, name)
    return left & right


@evaluate.register
def _(node: OrNode, name: str):
    left = evaluate(node.left, name)
    right = evaluate(node.right, name)
    return left | right


@evaluate.register
def _(node: NotNode, name: str):
    expr = evaluate(node.expr, name)
    return ~expr


@evaluate.register
def _(node: Operand, name: str):
    return Q(**{f"{name}__icontains": node.value})
