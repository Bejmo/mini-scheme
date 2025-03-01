(define (aplica-dos-cops f x)
  (f (f x)))

(define (incrementa x)
  (+ x 1))

(define (dobla x)
  (* x 2))

(define (main)
  (display "Resultat d'aplicar Incrementa dos cops a 5: ")
  (display (aplica-dos-cops incrementa 5))
  (newline)

  (display "Resultat d'aplicar Dobla dos cops a 2: ")
  (display (aplica-dos-cops dobla 2))
  (newline)

  ; Error: Llamar con argumento no función
  (display "Ha de donar un error al aplica 42 como una funció.")
  (display (aplica-dos-cops 42 5)) ; Dona error
  (newline))
