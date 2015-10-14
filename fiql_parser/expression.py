# -*- coding: utf-8 -*-
"""
FIQL BaseExpression and Expression.
"""
from __future__ import unicode_literals
from __future__ import absolute_import


from .exceptions import FiqlObjectException
from .operator import Operator


class BaseExpression(object):

    """
    FIQL Expression/Constraint base.

    Note:
        The parent of any child of BaseExpression is always an Expression.
        This is a bit contrary to what might be expected as an Expression
        itself is a child of BaseExpression. From a FIQL standpoint it
        makes perfect sense since a Constraint is a simple Expression
        itself. This is one of those many cases of the logic of a structure
        not being consistent with the logic required to implement it.

    Attributes:
        parent (Expression): The `Expression` which contains this object.
    """

    def __init__(self):
        """Initialize instance of BaseExpression."""
        self.parent = None

    def set_parent(self, parent):
        """Set parent Expression for this object.

        Args:
            parent (Expression): The Expression which contains this object.

        Raises:
            FiqlObjectException: Parent must be of type Expression.
        """
        if not isinstance(parent, Expression):
            raise FiqlObjectException("Parent must be of %s not %s" % (
                Expression, type(parent)))
        self.parent = parent

    def get_parent(self):
        """Get the parent Expression for this object.

        Returns:
            Expression: The Expression which contains this object.

        Raises:
            FiqlObjectException: Parent is None.
        """
        if not isinstance(self.parent, Expression):
            raise FiqlObjectException("Parent must be of %s not %s" % (
                Expression, type(self.parent)))
        return self.parent


class Expression(BaseExpression):

    """
    FIQL Expression.

    Both Constraint and Expression classes extend the BaseExpression class.
    This simplifies some parsing logic as most of the rules which apply to
    Constraints are equally applicable to Expressions.

    Attributes:
        elements (list): List of elements in this expression.
        operator (Operator): The operator which relates the elements in this
            expression.
    """

    def __init__(self):
        """Initialize instance of Expression."""
        super(Expression, self).__init__()
        self.elements = []
        self.operator = None
        # Keep track of which nested fragment we are in.
        self._working_fragment = self
        # Keep track of what was last added.
        self._last_element = None

    def has_constraint(self):
        """Return whether or not the working Expression has any Constraints."""
        return len(self.elements)

    def add_operator(self, operator):
        """Add an operator to the Expression.

        The Operator may result in a new expression if an operator already
        exists and is of a different precedence.

        There are three possibilities when adding an operator to an expression
        depending on whether or not an operator already exists.

          - No operator on the working expression; Simply set the operator and
            return self.
          - Operator already exists and is higher in precedence; The operator
            and last Constraint belong in a subexpression of the working
            expression.
          - Operator already exists and is lower in precedence; The operator
            belongs to the parent of the working expression whether one
            currently exists or not. To remain in the context of the top
            Expression, this method will return the parent here rather than
            self.

        Args:
            operator (Operator): What we are adding.

        Returns:
            Expression: self or related expression.

        Raises:
            FiqlObjectExpression: operator is not a valid Operator.
        """
        if not isinstance(operator, Operator):
            raise FiqlObjectException("%s is not a valid element type" % (
                operator.__class__))

        if not self._working_fragment.operator:
            self._working_fragment.operator = operator
        elif operator > self._working_fragment.operator:
            last_constraint = self._working_fragment.elements.pop()
            self._working_fragment = self._working_fragment \
                    .create_nested_expression()
            self._working_fragment.add_element(last_constraint)
            self._working_fragment.add_operator(operator)
        elif operator < self._working_fragment.operator:
            if self._working_fragment.parent:
                return self._working_fragment.parent.add_operator(operator)
            else:
                return Expression().add_element(self._working_fragment) \
                        .add_operator(operator)
        return self

    def add_element(self, element):
        """Add an element to the Expression.

        The element may be a Constraint, Expression, or Operator. This method
        contains logic to ensure that the expression starts with a Constraint
        or Expression and that there is always an Operator between any two
        Expressions/Constraints.

        Args:
            element: Constraint, Expression, or Operator.

        Returns:
            Expression: self

        Raises:
            FiqlObjectException: Element is not a valid type.
        """
        if isinstance(element, BaseExpression):
            element.set_parent(self._working_fragment)
            self._working_fragment.elements.append(element)
            return self
        else:
            return self.add_operator(element)

    def create_nested_expression(self):
        """Create a nested Expression, add it as an element to this Expression,
        and return it.

        Returns:
            Expression: The newly created nested Expression.
        """
        sub = Expression()
        self.add_element(sub)
        return sub

    def op_and(self, *elements):
        """Fluently add an 'AND' operator to the expression.

        Args:
            *elements (Expressions and/or Constraints): The elements which this
                operator applies to.

        Returns:
            Expression: self
        """
        expression = self.add_operator(Operator(';'))
        for element in elements:
            expression.add_element(element)
        return expression

    def op_or(self, *elements):
        """Fluently add an 'OR' operator to the expression.

        Args:
            *elements (Expressions and/or Constraints): The elements which this
                operator applies to.

        Returns:
            Expression: self
        """
        expression = self.add_operator(Operator(','))
        for element in elements:
            expression.add_element(element)
        return expression

    def to_python(self):
        """Return the Expression instance as list of tuples or tuple (If a
        single constraint).
        """
        if len(self.elements) == 0:
            return None
        if len(self.elements) == 1:
            return self.elements[0].to_python()
        operator = self.operator or Operator(';')
        return [operator.to_python()] + \
            [elem.to_python() for elem in self.elements]

    def __str__(self):
        """Return the Expression instance as a string."""
        operator = self.operator or Operator(';')
        elements_str = str(operator).join(
            ["{0}".format(elem) for elem in self.elements])
        if self.parent:
            parent_operator = self.parent.operator or Operator(';')
            if parent_operator > operator:
                return "(" + elements_str + ")"
        return elements_str

