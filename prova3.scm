; Diversos errors (cal anar eliminant les funcions de dalt per veure tots els missatges, ja que )

; Error: If sense l'expressió si el valor és fals
(define (condicional a b)
  (if (> a b)
      a))

(display (condicional 3 2)) ; Ha de donar error, perquè l'if no té una expressió a fer en la negativa.

; Error: Ús de variables no definides
(define (variables-no-definides)
  (+ a b))

; Error: no es poden definir funcions dins de funcions
(define (funcio-dins-de-funcio)
  (define (suma a b) (+ a b))
  (display (suma 3 4))
)

(define (main)
  (display "Prueba de errores"))
  (newline)
  (display (variables-no-definides))
  (funcio-dins-de-funcio)