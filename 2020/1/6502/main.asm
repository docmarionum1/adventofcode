;var = $99
;input = $1000

; Store the pointer to the current input at $00,$01
input_pointer_lsb = $00
input_pointer_msb = $01

; j is a copy of the input pointer for our loop that lives at $08,$09
j = $08
j_lsb = $08
j_msb = $09

; x is the number that we are comparing each other number to
x_lsb = $0a
x_msb = $0b

; sum is the number that we're trying to get to be 2020
sum_lsb = $0c
sum_msb = $0d

; product is a 4-byte number
product_0 = $10
product_1 = $11
product_2 = $12
product_3 = $13

; working memory for pow is at $02 (lsb), $03 (msb)
pow_lsb = $02
pow_msb = $03
pow_lsb_2 = $04
pow_msb_2 = $05

; working memory for _readNumber
readNumber_lsb = $06
readNumber_msb = $07



.org $C000

_init:
	; Initialize stack to FF
	ldx #$ff
	txs
	ldx #$00

_start:
		; Initialize a memory pointer at $0 and j to address $1000
		lda #$00
		sta $00
		sta j
		lda #$10
		sta $01
		sta j_msb

_mainLoop:
		; read the first number out of input
		jsr _readNumber

		; Transfer it to x
		lda readNumber_lsb
		sta x_lsb
		lda readNumber_msb
		sta x_msb

		; store the current input_pointer + y in j for the next loop
		clc
		tya
		adc input_pointer_lsb
		sta j_lsb
		lda input_pointer_msb
		adc #00 ; add 0 to add the carry bit
		sta j_msb



		_subLoop:
			; Read the next number
			jsr _readNumber

			; Sum x with the current number
			clc
			lda x_lsb
			adc readNumber_lsb
			sta sum_lsb
			lda x_msb
			adc readNumber_msb
			sta sum_msb

			;jmp _brk

			; check if the numbers sum to 2020 ($07E4)
			cmp #$07
			bne _notEqual
			lda sum_lsb
			cmp #$e4
			beq _equal

			_notEqual:
				; check if we've reached the last line (It's only a new line)
				lda ($00),Y
				cmp #10
				bne _subLoop ; not a new line, continue

				; otherwise, reset input_pointer with the last value in j and return to the main loop
				lda j_lsb
				sta input_pointer_lsb
				lda j_msb
				sta input_pointer_msb
				ldy #00

				jmp _mainLoop

				;jmp _subLoop

		_equal:
			; Multiply x * readNumber
			; Multiplication algorithm from:
			; https://codebase64.org/doku.php?id=base:16bit_multiplication_32-bit_product
			ldx #16
			_shift_r:
				lsr x_msb
				ror x_lsb
				bcc _rotate_r
				lda product_2
				clc
				adc readNumber_lsb
				sta product_2
				lda product_3
				adc readNumber_msb
			_rotate_r:
				ror
				sta product_3
				ror product_2
				ror product_1
				ror product_0
				dex
				bne _shift_r

			jmp _brk

		;brk
		;jsr _readNumber
		;jsr _readNumber
		jmp _brk
		; pull one byte off of the input to check if
		;jsr _readNumber
		;brk

		; test _pow
		;lda #03
		;sta pow_lsb
		;lda #03
		;tax
		;jsr _pow

_end:

		BRK ; Break to tell our emulator to stop

_pow:
	; multiply a 1-digit number by 10^x power, outputs a 2-byte number
	; input
	; pow_lsb = 1-9
	; x = 0, 1, 2, 3

	; Save x on the stack
	txa
	pha

	; clear working memory
	lda #00
	sta pow_msb
	sta pow_lsb_2
	sta pow_msb_2

	; Check if x is 0, if so, return
	cpx #00
	beq _powEnd

	; store the pow_lsb on the stack while we raise 10 to x
	lda pow_lsb
	; check if this value is 0, if so return.
	beq _powEnd

	pha
	lda #00
	sta pow_lsb

	; raise 10 to the x
	; we know that our inputs are at most 4 digits, so we can hardcode the results for
	; 10^1, 10^2 and 10^3. This will be more efficent than looping since 6502 can't
	; multiply

	cpx #01
	bne _powNot1
	lda #10
	sta pow_lsb_2
	jmp _powMul

	_powNot1:
	cpx #02
	bne _powNot2
	lda #100
	sta pow_lsb_2
	jmp _powMul

	; We know from our data that this will be true if it wasn't 0, 1 or 2
	_powNot2:
	lda #$E8
	sta pow_lsb_2
	lda #$3
	sta pow_msb_2

	; multiply the value in pow_lsb, pow_msb by the value that was in pow_lsb when _pow was called
	; This will be done by adding the value in pow_* to itself x times
	_powMul:
	; We saved that value on the stack, so pull it back off into x
	pla
	tax

	_powMulLoop:
		clc

		lda pow_lsb
		adc pow_lsb_2
		sta pow_lsb

		lda pow_msb
		adc pow_msb_2
		sta pow_msb

		dex
		bne _powMulLoop

	_powEnd:
		; restore x from the stack
		pla
		tax
		rts

_readNumber:
		; Read an ascii number out of input and convert it into a 16-bit number
		; Address should be in memory at $00

		; save the registers we'll use on the stack
		php
		pha
		txa
		pha

		; clear the readNumber working memory
		lda #00
		sta readNumber_lsb
		sta readNumber_msb

		; Put a newline on the stack to mark the beginning of the number
		lda #10
		pha

		; loop through the bytes until we hit a new line
		_readNumberLoop:
			lda ($00),Y ; Load the current byte into A
			pha ; store the byte on the stack
			;inx ; increment x and y

			; Increment y
			iny

			; Check if Y hit 255, in this case we need to increment the value at $01
			bne _readNumberOverflowY
			inc $01
			_readNumberOverflowY

			cmp #10 ; Check if it's a new line
			bne _readNumberLoop ; go back to the begining of the loop if it's not

		pla ; pull the new line off of the stack

		; Now we need to iterate backwards to convert the characters to a number, starting
		; with the least significant digit
		ldx #00 ; Use x to keep track of the current digit

		_readNumberLoop2:
			pla
			cmp #10 ; Check if it's a new line
			beq _readNumberEnd ; if it's a new line, we're done

			sbc #$30 ; subtract 30 to turn it into a number

			; transfer the digit to pow_lsb and call _pow
			sta pow_lsb
			jsr _pow

			; add the new value to the existing value
			clc
			lda readNumber_lsb
			adc pow_lsb
			sta readNumber_lsb
			lda readNumber_msb
			adc pow_msb
			sta readNumber_msb

			; increment x and jump back to the beginning of the loop
			inx
			jmp _readNumberLoop2

		_readNumberEnd:
			; Pop x back off of the stack and return
			pla
			tax
			pla
			plp
			rts

_brk:
	nop
	nop
