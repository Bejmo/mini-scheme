; Suma dos nombres
(define (suma a b)
  (+ a b))

; Funció amb 3 paràmetres, però es crida amb 2
(define (producte a b c)
  (* a b))

(define (main)
  (display "Introdueix dos números: ")
  (newline)
  (let ((n1 (read))
        (n2 (read)))
    (display "Suma: ")
    (display (suma n1 n2))
    (newline)
    (display (producte n1 n2)) ; Això dona error perquè no es crida amb tots els paràmetres
    (newline)
  )
)