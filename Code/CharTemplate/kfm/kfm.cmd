; The CMD file.
;
; Two parts: 1. Command definition and  2. State entry
; (state entry is after the commands def section)
;
; 1. Command definition
; ---------------------
; Note: The commands are CASE-SENSITIVE, and so are the command names.
; The eight directions are:
;   B, DB, D, DF, F, UF, U, UB     (all CAPS)
;   corresponding to back, down-back, down, downforward, etc.
; The six buttons are:
;   a, b, c, x, y, z               (all lower case)
;   In default key config, abc are are the bottom, and xyz are on the
;   top row. For 2 button characters, we recommend you use a and b.
;   For 6 button characters, use abc for kicks and xyz for punches.
;
; Each [Command] section defines a command that you can use for
; state entry, as well as in the CNS file.
; The command section should look like:
;
;   [Command]
;   name = some_name
;   command = the_command
;   time = time (optional)
;   buffer.time = time (optional)
;
; - some_name
;   A name to give that command. You'll use this name to refer to
;   that command in the state entry, as well as the CNS. It is case-
;   sensitive (QCB_a is NOT the same as Qcb_a or QCB_A).
;
; - command
;   list of buttons or directions, separated by commas. Each of these
;   buttons or directions is referred to as a "symbol".
;   Directions and buttons can be preceded by special characters:
;   slash (/) - means the key must be held down
;          egs. command = /D       ;hold the down direction
;               command = /DB, a   ;hold down-back while you press a
;   tilde (~) - to detect key releases
;          egs. command = ~a       ;release the a button
;               command = ~D, F, a ;release down, press fwd, then a
;          If you want to detect "charge moves", you can specify
;          the time the key must be held down for (in game-ticks)
;          egs. command = ~30a     ;hold a for at least 30 ticks, then release
;   dollar ($) - Direction-only: detect as 4-way
;          egs. command = $D       ;will detect if D, DB or DF is held
;               command = $B       ;will detect if B, DB or UB is held
;   plus (+) - Buttons only: simultaneous press
;          egs. command = a+b      ;press a and b at the same time
;               command = x+y+z    ;press x, y and z at the same time
;   greater-than (>) - means there must be no other keys pressed or released
;                      between the previous and the current symbol.
;          egs. command = a, >~a   ;press a and release it without having hit
;                                  ;or released any other keys in between
;   You can combine the symbols:
;     eg. command = ~30$D, a+b     ;hold D, DB or DF for 30 ticks, release,
;                                  ;then press a and b together
;
;   Note: Successive direction symbols are always expanded in a manner similar
;         to this example:
;           command = F, F
;         is expanded when MUGEN reads it, to become equivalent to:
;           command = F, >~F, >F
;
;   It is recommended that for most "motion" commads, eg. quarter-circle-fwd,
;   you start off with a "release direction". This makes the command easier
;   to do.
;
; - time (optional)
;   Time allowed to do the command, given in game-ticks. The default
;   value for this is set in the [Defaults] section below. A typical
;   value is 15.
;
; - buffer.time (optional)
;   Time that the command will be buffered for. If the command is done
;   successfully, then it will be valid for this time. The simplest
;   case is to set this to 1. That means that the command is valid
;   only in the same tick it is performed. With a higher value, such
;   as 3 or 4, you can get a "looser" feel to the command. The result
;   is that combos can become easier to do because you can perform
;   the command early. Attacks just as you regain control (eg. from
;   getting up) also become easier to do. The side effect of this is
;   that the command is continuously asserted, so it will seem as if
;   you had performed the move rapidly in succession during the valid
;   time. To understand this, try setting buffer.time to 30 and hit
;   a fast attack, such as KFM's light punch.
;   The default value for this is set in the [Defaults] section below.
;   This parameter does not affect hold-only commands (eg. /F). It
;   will be assumed to be 1 for those commands.
;
; If you have two or more commands with the same name, all of them will
; work. You can use it to allow multiple motions for the same move.
;
; Some common commands examples are given below.
;
; [Command] ;Quarter circle forward + x
; name = "QCF_x"
; command = ~D, DF, F, x
;
; [Command] ;Half circle back + a
; name = "HCB_a"
; command = ~F, DF, D, DB, B, a
;
; [Command] ;Two quarter circles forward + y
; name = "2QCF_y"
; command = ~D, DF, F, D, DF, F, y
;
; [Command] ;Tap b rapidly
; name = "5b"
; command = b, b, b, b, b
; time = 30
;
; [Command] ;Charge back, then forward + z
; name = "charge_B_F_z"
; command = ~60$B, F, z
; time = 10
;
; [Command] ;Charge down, then up + c
; name = "charge_D_U_c"
; command = ~60$D, U, c
; time = 10


;-| Button Remapping |-----------------------------------------------------
; This section lets you remap the player's buttons (to easily change the
; button configuration). The format is:
;   old_button = new_button
; If new_button is left blank, the button cannot be pressed.
[Remap]
x = x
y = y
z = z
a = a
b = b
c = c
s = s

;-| Default Values |-------------------------------------------------------
[Defaults]
; Default value for the "time" parameter of a Command. Minimum 1.
command.time = 15

; Default value for the "buffer.time" parameter of a Command. Minimum 1,
; maximum 30.
command.buffer.time = 1


;-| Super Motions |--------------------------------------------------------
;The following two have the same name, but different motion.
;Either one will be detected by a "command = TripleKFPalm" trigger.
;Time is set to 20 (instead of default of 15) to make the move
;easier to do.
;
[Command]
name = "TripleKFPalm"
command = ~D, DF, F, D, DF, F, x
time = 20

[Command]
name = "TripleKFPalm"   ;Same name as above
command = ~D, DF, F, D, DF, F, y
time = 20

[Command]
name = "SmashKFUpper"
command = ~D, DB, B, D, DB, B, x;~F, D, DF, F, D, DF, x
time = 20

[Command]
name = "SmashKFUpper"   ;Same name as above
command = ~D, DB, B, D, DB, B, y;~F, D, DF, F, D, DF, y
time = 20

;-| Special Motions |------------------------------------------------------
[Command]
name = "blocking"
command = $F,x
time = 3

[Command]
name = "blocking" ;Same name as above (buttons in opposite order)
command = x,$F
time = 3

[Command]
name = "upper_x"
command = ~F, D, DF, x

[Command]
name = "upper_y"
command = ~F, D, DF, y

[Command]
name = "upper_xy"
command = ~F, D, DF, x+y

[Command]
name = "QCF_x"
command = ~D, DF, F, x

[Command]
name = "QCF_y"
command = ~D, DF, F, y

[Command]
name = "QCF_xy"
command = ~D, DF, F, x+y

[Command]
name = "QCB_x"
command = ~D, DB, B, x

[Command]
name = "QCB_y"
command = ~D, DB, B, y

[Command]
name = "QCB_xy"
command = ~D, DB, B, x+y

[Command]
name = "QCF_a"
command = ~D, DF, F, a

[Command]
name = "QCF_b"
command = ~D, DF, F, b

[Command]
name = "QCF_ab"
command = ~D, DF, F, a+b

[Command]
name = "FF_ab"
command = F, F, a+b

[Command]
name = "FF_a"
command = F, F, a

[Command]
name = "FF_b"
command = F, F, b

;-| Double Tap |-----------------------------------------------------------
[Command]
name = "FF"     ;Required (do not remove)
command = F, F
time = 10

[Command]
name = "BB"     ;Required (do not remove)
command = B, B
time = 10

;-| 2/3 Button Combination |-----------------------------------------------
[Command]
name = "recovery";Required (do not remove)
command = x+y
time = 1

;-| Dir + Button |---------------------------------------------------------
[Command]
name = "down_a"
command = /$D,a
time = 1

[Command]
name = "down_b"
command = /$D,b
time = 1

;-| Single Button |---------------------------------------------------------
[Command]
name = "a"
command = a
time = 1

[Command]
name = "b"
command = b
time = 1

[Command]
name = "c"
command = c
time = 1

[Command]
name = "x"
command = x
time = 1

[Command]
name = "y"
command = y
time = 1

[Command]
name = "z"
command = z
time = 1

[Command]
name = "start"
command = s
time = 1

;-| Hold Dir |--------------------------------------------------------------
[Command]
name = "holdfwd";Required (do not remove)
command = /$F
time = 1

[Command]
name = "holdback";Required (do not remove)
command = /$B
time = 1

[Command]
name = "holdup" ;Required (do not remove)
command = /$U
time = 1

[Command]
name = "holddown";Required (do not remove)
command = /$D
time = 1

;---------------------------------------------------------------------------
; 2. State entry
; --------------
; This is where you define what commands bring you to what states.
;
; Each state entry block looks like:
;   [State -1, Label]           ;Change Label to any name you want to use to
;                               ;identify the state with.
;   type = ChangeState          ;Don't change this
;   value = new_state_number
;   trigger1 = command = command_name
;   . . .  (any additional triggers)
;
; - new_state_number is the number of the state to change to
; - command_name is the name of the command (from the section above)
; - Useful triggers to know:
;   - statetype
;       S, C or A : current state-type of player (stand, crouch, air)
;   - ctrl
;       0 or 1 : 1 if player has control. Unless "interrupting" another
;                move, you'll want ctrl = 1
;   - stateno
;       number of state player is in - useful for "move interrupts"
;   - movecontact
;       0 or 1 : 1 if player's last attack touched the opponent
;                useful for "move interrupts"
;
; Note: The order of state entry is important.
;   State entry with a certain command must come before another state
;   entry with a command that is the subset of the first.
;   For example, command "fwd_a" must be listed before "a", and
;   "fwd_ab" should come before both of the others.
;
; For reference on triggers, see CNS documentation.
;
; Just for your information (skip if you're not interested):
; This part is an extension of the CNS. "State -1" is a special state
; that is executed once every game-tick, regardless of what other state
; you are in.


; Don't remove the following line. It's required by the CMD standard.
[Statedef -1]

; AI switch -> ON
[State -1, Activate AI]
type = Varset
triggerall = var(59) != 1
trigger1 = command = "TripleKFPalm"
trigger2 = command = "SmashKFUpper"
trigger3 = command = "blocking"
trigger4 = command = "upper_x"
trigger5 = command = "upper_y"
trigger6 = command = "upper_xy"
trigger7 = command = "QCF_x"
trigger8 = command = "QCF_y"
trigger9 = command = "QCF_xy"
trigger10 = command = "QCF_a"
trigger11 = command = "QCF_b"
trigger12 = command = "QCF_ab"
trigger13 = command = "FF_ab"
trigger14 = command = "FF_a"
trigger15 = command = "FF_b"
trigger16 = command = "FF"
trigger17 = command = "BB"
trigger18 = command = "recovery"
trigger19 = command = "down_a"
trigger20 = command = "down_b"
trigger21 = command = "a"
trigger22 = command = "b"
trigger23 = command = "c"
trigger24 = command = "x"
trigger25 = command = "y"
trigger26 = command = "z"
trigger27 = command = "start"
trigger28 = command = "holdfwd"
trigger29 = command = "holdback"
trigger30 = command = "holdup"
trigger31 = command = "holddown"
v = 59
value = 1

;++++++++++++++++++++++


;---------------------------------------------------------------------------
;---------------------------------------------------------------------------
;Crouching Strong Kick
[State -1, Crouching Strong Kick]
type = ChangeState
value = 440
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2MoveType = I
trigger1 = InGuardDist = 1

;---------------------------------------------------------------------------
;High Kung Fu Blocking (Low)
[State -1, High Kung Fu Blocking Low]
type = ChangeState
value = 1320
triggerall = roundstate = 2
triggerall = random < 500

triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2BodyDist y = [30,60]
trigger1 = MoveGuarded = 0
trigger1 = P2BodyDist x = [30,100]

;---------------------------------------------------------------------------
;Light Kung Fu Upper
[State -1, Light Kung Fu Upper]
type = ChangeState
value = 1100
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2BodyDist y = [30,60]
trigger1 = P2BodyDist x = [30,100]

;---------------------------------------------------------------------------
;Strong Kung Fu Palm
[State -1, Strong Kung Fu Palm]
type = ChangeState
value = 1010
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveContact = 0 
trigger1 = P2StateType = A
trigger1 = P2BodyDist x = [30,100]

;---------------------------------------------------------------------------
;Fast Kung Fu Upper (1/3 super bar)
[State -1, Fast Kung Fu Upper]
type = ChangeState
value = 1120
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = InGuardDist = 0
trigger1 = MoveContact != 0
trigger1 = P2BodyDist y = [-60,-1]
trigger1 = P2MoveType = A

;---------------------------------------------------------------------------
;Smash Kung Fu Upper (uses one super bar)
[State -1, Smash Kung Fu Upper]
type = ChangeState
value = 3050
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveContact = 0 
trigger1 = InGuardDist = 1
trigger1 = P2StateType = C

;---------------------------------------------------------------------------
;Stand Light Punch
[State -1, Stand Light Punch]
type = ChangeState
value = 200
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveContact = 0 
trigger1 = InGuardDist = 1
trigger1 = MoveGuarded = 0
trigger1 = P2BodyDist y = [-60,-1]

;---------------------------------------------------------------------------
;Fast Kung Fu Palm (1/3 super bar)
[State -1, Fast Kung Fu Palm]
type = ChangeState
value = 1020
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveContact = 0 
trigger1 = P2BodyDist y = [30,60]

;---------------------------------------------------------------------------
;Strong Kung Fu Upper
[State -1, Strong Kung Fu Upper]
type = ChangeState
value = 1110
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = InGuardDist = 0
trigger1 = P2BodyDist y = [-60,-1]

;---------------------------------------------------------------------------
;Taunt
[State -1, Taunt]
type = ChangeState
value = 195
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveGuarded = 0
trigger1 = InGuardDist = 0

;---------------------------------------------------------------------------
;High Kung Fu Blocking (High)
[State -1, High Kung Fu Blocking High]
type = ChangeState
value = 1300
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2MoveType = A
trigger1 = InGuardDist = 1

;---------------------------------------------------------------------------
;Fast Kung Fu Knee (1/3 super bar)
[State -1, Fast Kung Fu Knee]
type = ChangeState
value = 1070
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2MoveType = H
trigger1 = P2BodyDist x = [0,30]

;---------------------------------------------------------------------------
;Kung Fu Throw
[State -1, Kung Fu Throw]
type = ChangeState
value = 800
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveGuarded = 0
trigger1 = P2BodyDist x = [100,200]

;---------------------------------------------------------------------------
;Light Kung Fu Knee
[State -1, Light Kung Fu Knee]
type = ChangeState
value = 1050
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveGuarded = 0
trigger1 = InGuardDist = 1

;---------------------------------------------------------------------------
;Jump Light Kick
[State -1, Jump Light Kick]
type = ChangeState
value = 630
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = InGuardDist = 0
trigger1 = P2StateType = S
trigger1 = MoveGuarded = 0

;---------------------------------------------------------------------------
;Strong Kung Fu Blow
[State -1, Strong Kung Fu Blow]
type = ChangeState
value = 1210
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = InGuardDist = 1
trigger1 = MoveContact = 0 
trigger1 = P2StateType = S
trigger1 = P2MoveType = H

;---------------------------------------------------------------------------
;Standing Strong Kick
[State -1, Standing Strong Kick]
type = ChangeState
value = 240
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2BodyDist y = [-60,-1]

;---------------------------------------------------------------------------
;Run Fwd
[State -1, Run Fwd]
type = ChangeState
value = 100
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = InGuardDist = 1
trigger1 = P2MoveType = H

;---------------------------------------------------------------------------
;Crouching Light Punch
[State -1, Crouching Light Punch]
type = ChangeState
value = 400
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveContact = 0 
trigger1 = P2MoveType = A
trigger1 = P2BodyDist x = [0,30]

;---------------------------------------------------------------------------
;Crouching Light Kick
[State -1, Crouching Light Kick]
type = ChangeState
value = 430
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2BodyDist y = [-60,-1]

;---------------------------------------------------------------------------
;Light Kung Fu Blow
[State -1, Light Kung Fu Blow]
type = ChangeState
value = 1200
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2MoveType = H
trigger1 = P2BodyDist y = [30,60]
trigger1 = P2StateType = C

;---------------------------------------------------------------------------
;High Kung Fu Blocking (Air)
[State -1, High Kung Fu Blocking Low]
type = ChangeState
value = 1340
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveContact = 0 
trigger1 = P2BodyDist x = [30,100]

;---------------------------------------------------------------------------
;Light Kung Fu Zankou
[State -1, Light Kung Fu Zankou]
type = ChangeState
value = 1400
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2MoveType = A
trigger1 = P2BodyDist y = [-60,-1]

;---------------------------------------------------------------------------
;Jump Strong Punch
[State -1, Jump Strong Punch]
type = ChangeState
value = 610
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2StateType = C
trigger1 = MoveContact = 0 
trigger1 = P2BodyDist x = [100,200]
trigger1 = P2BodyDist y = [30,60]

;---------------------------------------------------------------------------
;Light Kung Fu Palm
[State -1, Light Kung Fu Palm]
type = ChangeState
value = 1000
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2MoveType = A
trigger1 = P2StateType = C
trigger1 = P2BodyDist x = [30,100]

;---------------------------------------------------------------------------
;Jump Strong Kick
[State -1, Jump Strong Kick]
type = ChangeState
value = 640
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2MoveType = H
trigger1 = MoveContact = 0 
trigger1 = P2BodyDist x = [30,100]

;---------------------------------------------------------------------------
;Strong Kung Fu Knee
[State -1, Strong Kung Fu Knee]
type = ChangeState
value = 1060
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2BodyDist x = [100,200]
trigger1 = P2MoveType = A
trigger1 = P2StateType = A
trigger1 = InGuardDist = 1

;---------------------------------------------------------------------------
;Strong Kung Fu Zankou
[State -1, Strong Kung Fu Zankou]
type = ChangeState
value = 1410
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = InGuardDist = 1
trigger1 = P2StateType = S
trigger1 = P2MoveType = A

;---------------------------------------------------------------------------
;Jump Light Punch
[State -1, Jump Light Punch]
type = ChangeState
value = 600
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2StateType = C
trigger1 = MoveGuarded != 0
trigger1 = P2MoveType = I
trigger1 = P2BodyDist x = [100,200]

;---------------------------------------------------------------------------
;Fast Kung Fu Blow (1/3 super bar)
[State -1, Fast Kung Fu Blow]
type = ChangeState
value = 1220
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2BodyDist y = [30,60]
trigger1 = MoveGuarded != 0

;---------------------------------------------------------------------------
;Stand Light Kick
[State -1, Stand Light Kick]
type = ChangeState
value = 230
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2BodyDist x = [100,200]

;---------------------------------------------------------------------------
;Stand Strong Punch
[State -1, Stand Strong Punch]
type = ChangeState
value = 210
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2MoveType = A
trigger1 = P2BodyDist y = [30,60]
trigger1 = MoveGuarded != 0
trigger1 = P2StateType = A

;---------------------------------------------------------------------------
;Crouching Strong Punch
[State -1, Crouching Strong Punch]
type = ChangeState
value = 410
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = InGuardDist = 0
trigger1 = P2BodyDist y = [30,60]

;---------------------------------------------------------------------------
;Triple Kung Fu Palm (uses one super bar)
[State -1, Triple Kung Fu Palm]
type = ChangeState
value = 3000
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2BodyDist x = [30,100]
trigger1 = P2BodyDist y = [30,60]
trigger1 = P2StateType = A
trigger1 = MoveGuarded != 0

;---------------------------------------------------------------------------
;Far Kung Fu Zankou
[State -1, Far Kung Fu Zankou]
type = ChangeState
value = 1420
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = MoveGuarded != 0

;---------------------------------------------------------------------------
;Run Back
[State -1, Run Back]
type = ChangeState
value = 105
triggerall = roundstate = 2
triggerall = random < 500
triggerall = var(59) = 1 
triggerall = Ctrl 
trigger1 = P2StateType = S
trigger1 = InGuardDist = 0
trigger1 = MoveContact = 0 
trigger1 = MoveGuarded != 0




;++++++++++++++++++
