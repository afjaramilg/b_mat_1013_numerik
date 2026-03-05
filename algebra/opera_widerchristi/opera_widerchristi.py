import field_pols as fp
import modulo_pols as mod_pols
from writers import polynomial_writer
import galois
import multiprocessing as mp



if __name__ == '__main__':
    fields = [2, 3, 4, 5, 7, 8];
    moduli = list(range(2, 9))
    degrees = [i for i in range(1, 5)]

    manager = mp.Manager()

    for deg in degrees: 
        for field_size in fields:
            field = galois.GF(field_size);

            print(f"now doing F_{field_size} with deg {deg}")

            all_gen = fp.yield_polynomials(deg, field, poly_type="all")
            re_count = 0
            irr_count = 0

            for i, (p, is_irred) in enumerate(all_gen):
                with open(f"field_output/F_{field_size}_{deg}_irr.txt", 'w') as irr:
                        if is_irred:
                            print(f"{str(p)}", file=irr )
                            irr_count += 1
                
            print(f"irreducible: {irr_count}, reducible: {re_count}")
                    
        
        print("NOW DOING MODULI")
        
        for modulo in moduli:
            q_reducible = manager.Queue()
            q_irreducible = manager.Queue()
         
            writer_irred = mp.Process(
                    target=polynomial_writer,
                    args=(q_irreducible, f"output_mods/Z_{modulo}_{deg}_irr.txt", "irreducible")
            )

            writer_red = mp.Process(
                    target=polynomial_writer,
                    args=(q_reducible, f"output_mods/Z_{modulo}_{deg}_re.txt", "reducible")
            )
           
            writer_irred.start()
            writer_red.start()
            
            mod_pols.compute_ring_polynomials_fast(deg, modulo, q_reducible, q_irreducible)

            q_reducible.put("DONE")
            q_irreducible.put("DONE")
            
            writer_red.join()
            writer_irred.join()
     



    print("Tibi dabo potestatem hanc universam, et gloriam illorum: quia mihi tradita sunt, et cui volo do illa. Tu ergo si adoraveris coram me, erunt tua omnia.")
