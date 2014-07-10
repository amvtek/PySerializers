namespace py thrift

enum Enum4 {
    VAL_0 = 0, 
    VAL_1 = 1, 
    VAL_2 = 2, 
    VAL_3 = 3
}

enum Enum16 {
    VAL_4 = 4, 
    VAL_5 = 5, 
    VAL_6 = 6, 
    VAL_7 = 7,
    VAL_8 = 8, 
    VAL_9 = 9, 
    VAL_10 = 10, 
    VAL_11 = 11,
    VAL_12 = 12, 
    VAL_13 = 13, 
    VAL_14 = 14, 
    VAL_15 = 15,
    VAL_16 = 16, 
    VAL_17 = 17, 
    VAL_18 = 18, 
    VAL_19 = 19
}

struct NumStuff {

    1:i32 i01,
    2:i64 i02,
    3:double d03,
    4:Enum4 e_04,
    5:list<i64> l1_i05,
    6:list<double> l1_d06,
    7:list<Enum16> l1_e07
}

struct StringStuff {

    1: string s01,
    2: binary b02,
    3: list<string> l1_s03,
    4: list<binary> l1_b04
}

struct ComboStuff {

    1: i32 i01,
    2: i64 i02,
    3: double d03,
    4: Enum4 e_04,
    5: list<i64> l1_i05,
    6: list<double> l1_d06,
    7: list<Enum16> l1_e07,
    8: string s08,
    9: binary b09,
    10: list<string> l1_s10,
    11: list<binary> l1_b11
}

struct ComboBunch {

    1: Enum16 e_01,
    2: NumStuff ns02,
    3: StringStuff ss03,
    4: ComboStuff cs04,
    5: list<NumStuff> l2_ns05,
    6: list<StringStuff> l2_ss06,
    7: list<ComboStuff> l2_cs07
}
