(define (calcula a b)
  (let ((suma (+ a b))
        (resta (- a b))
        (producte (* a b)))
    (let ((resultat (if (> resta 0)
                         (+ suma producte)
                         (- resta producte))))
      resultat)))

(define (main)
  (display "Resultat de calcular(4, 2): ") ; Ha de donar 14
  (display (calcula 4 2))
  (newline)
  (display "Resultat de calcula(2, 4): ") ; Ha de donar -10
  (display (calcula 2 4))
  (newline))