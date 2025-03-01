; Prova 1: recursivitat, llistes i operacions
; @TODO hacer que dependiendo del input, haga una operación u otra
(define (suma-llista l)
  (if (null? l)
      0
      (+ (car l) (suma-llista (cdr l)))))

(define (maxim l)
  (if (null? (cdr l))
      (car l)
      (let ((resta (maxim (cdr l))))
        (if (> (car l) resta)
            (car l)
            resta))))

(define (procesa-lista l)
  (let ((suma (suma-llista l))
        (max (maxim l)))
    (display "Suma: ")
    (display suma)
    (newline)
    (display "Màxim: ")
    (display max)
    (newline)))

(define (main)
  (let ((lista '(3 1 4 1 5 9 2 6 5)))
    (procesa-lista lista)))