---
description: 'OpenCog Scheme/Guile coding standards and patterns. Activates for .scm files.'
applyTo: '**/*.scm'
---

# OpenCog Scheme Coding Standards

## AtomSpace Scheme API
```scheme
;; Node creation
(cog-new-node 'ConceptNode "name")
(Concept "name")  ; shorthand

;; Link creation  
(cog-new-link 'InheritanceLink (Concept "A") (Concept "B"))
(Inheritance (Concept "A") (Concept "B"))  ; shorthand

;; Execution
(cog-execute! (Bind ...))
(cog-evaluate! (Satisfaction ...))

;; Query
(cog-incoming-set atom)
(cog-outgoing-set atom)
(cog-get-atoms 'ConceptNode)
```

## URE Rule Pattern
```scheme
(DefineLink
  (DefinedSchemaNode "rule-name")
  (BindLink
    (VariableList ...)
    (AndLink ...)     ; premises
    (ExecutionOutputLink
      (GroundedSchemaNode "scm: formula-name")
      (ListLink ...))))  ; conclusion
```

## Module Structure
- Use `(define-module (opencog component-name))`
- Export with `#:export (fn1 fn2 fn3)`
- Load deps: `(use-modules (opencog atomspace))`
- Files must be >200 bytes (no stubs/placeholders)

## Truth Values
```scheme
(cog-new-stv strength confidence)  ; Simple TV
(stv 0.9 0.8)                      ; Shorthand
(cog-tv atom)                      ; Get TV
(cog-mean atom)                    ; Get mean/strength
(cog-confidence atom)              ; Get confidence
```
