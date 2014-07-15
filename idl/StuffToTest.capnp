# capnp forces the use of camel case over underscore
# if underscore are used, schema will not compile :(
@0x8896055ced17c8e7;


enum Enum4 {
    val0 @0;
    val1 @1;
    val2 @2;
    val3 @3;
}

enum Enum16 {
    ign0 @0;
    ign1 @1;
    ign2 @2;
    ign3 @3;
    val4 @4;
    val5 @5;
    val6 @6;
    val7 @7;
    val8 @8;
    val9 @9;
    val10 @10;
    val11 @11;
    val12 @12;
    val13 @13;
    val14 @14;
    val15 @15;
    val16 @16;
    val17 @17;
    val18 @18;
    val19 @19;
}

struct NumStuff {

    i01 @0: Int32;

    i02 @1: Int64;

    d03 @2: Float64;

    e04 @3: Enum4;

    l1i05 @4: List(Int64);

    l1d06 @5: List(Float64);

    l1e07 @6: List(Enum16);

}

struct StringStuff {

    s01 @0: Text;

    b02 @1: Data;

    l1s03 @2: List(Text);

    l1b04 @3: List(Data);
}

struct ComboStuff {

    i01 @0: Int32;

    i02 @1: Int64;

    d03 @2: Float64;

    e04 @3: Enum4;

    l1i05 @4: List(Int64);

    l1d06 @5: List(Float64);

    l1e07 @6: List(Enum16);
    
    s08 @7: Text;

    b09 @8: Data;

    l1s10 @9: List(Text);

    l1b11 @10: List(Data);
}


struct ComboBunch {

    e01 @0: Enum16;

    ns02 @1: NumStuff;

    ss03 @2: StringStuff;

    cs04 @3: ComboStuff;

    l2ns05 @4: List(NumStuff);

    l2ss06 @5: List(StringStuff);

    l2cs07 @6: List(ComboStuff);
}
