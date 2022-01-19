package fr.univ.test_apk_analyse_1_ok.inheritance;

public abstract class Canide extends Animal {
    public Canide(){
        super();
        System.out.println("Bonjour depuis Canide");
    }

    public void canideSound(){
        System.out.println("Canide sound");
    }
}
