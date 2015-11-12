// Grupo 3
// Alberto Lorente
// Hristo Ivanov

 /**
 * Adaptación del ejemplo original en http://wiki.apache.org/hadoop/WordCount
 */

import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


import org.apache.hadoop.mapreduce.lib.input.FileSplit;
import java.util.HashMap;
import java.util.Map;
import org.apache.hadoop.io.Writable;
import java.io.DataInput;
import java.io.DataOutput;

/**
 * <p>Este ejemplo cuenta el número de veces que aparece cada palabra en el 
 * archivo de entrada usando MapReduce. El código tiene 3 partes: mapper, 
 * reduce y programa principal</p>
 */
public class eje_4 {

  public static class Composite3Writable implements Writable {
    int val1 = 0;
    int val2 = 0;
    int val3 = 0;

    public Composite3Writable() {}

    public Composite3Writable(int val1, int val2, int val3) {
        this.val1 = val1;
        this.val2 = val2;
        this.val3 = val3;
    }

    @Override
    public void readFields(DataInput in) throws IOException {
        val1 = in.readInt();
        val2 = in.readInt();
        val3 = in.readInt();
    }

    @Override
    public void write(DataOutput out) throws IOException {
        out.writeInt(val1);
        out.writeInt(val2);
        out.writeInt(val3);
    }

    @Override
    public String toString() {
        return this.val1 + "\t" + this.val2 + "\t" + this.val3;
    }
  }



  /**
   * <p>
   * El mapper extiende de la interfaz org.apache.hadoop.mapreduce.Mapper. Cuando
   * se ejecuta Hadoop el mapper recibe cada linea del archivo de entrada como
   * argumento. La función "map" parte cada línea y para cada palabra emite la
   * pareja (word,1) como salida.</p>
   */
  public static class TokenizerMapper 
       extends Mapper<Object, Text, Text, Composite3Writable>{
    
    private Text r_key = new Text();
      
    public void map(Object key, Text value, Context context
                    ) throws IOException, InterruptedException {
      
      String[] word = value.toString().replaceAll("\".*\"", "").replaceAll(" +", " ").split(" ");

      if (word[3].equals("-")) word[3] = "0";
      if (word[2].matches("4..") || word[2].matches("5..")) word[2] = "1";
      else word[2] = "0";

      Composite3Writable val = new Composite3Writable( 1, Integer.parseInt(word[3]), Integer.parseInt(word[2]));
      r_key.set(word[0]);
      context.write(r_key, val);
    }
  }
  
  /**
   * <p>La función "reduce" recibe los valores (apariciones) asociados a la misma
   * clave (palabra) como entrada y produce una pareja con la palabra y el número
   * total de apariciones. 
   * Ojo: como las parejas generadas por la función "map" siempre tienen como 
   * valor 1 se podría evitar la suma y devolver directamente el número de 
   * elementos.</p>  
   */
  public static class IntSumReducer 
       extends Reducer<Text,  Composite3Writable, Text, Composite3Writable> {

    private Text result = new Text();

    public void reduce(Text key, Iterable<Composite3Writable> values, 
                       Context context
                       ) throws IOException, InterruptedException {

      // yield key, map(sum,zip(*values))

      int var1=0, var2=0, var3=0;
      for (Composite3Writable val : values){
          var1 += val.val1;
          var2 += val.val2;
          var3 += val.val3;
      }
      Composite3Writable val = new Composite3Writable( var1, var2, var3);      

      context.write(key, val);
    }

  }

  /**
   * <p>Clase principal con método main que iniciará la ejecución de la tarea</p>
   */
  public static void main(String[] args) throws Exception {
    JobConf conf = new JobConf();
    Job job = Job.getInstance(conf);
    job.setJarByClass(eje_4.class);
    job.setMapperClass(TokenizerMapper.class);
    //Si existe combinador
    //job.setCombinerClass(Clase_del_combinador.class);
    job.setReducerClass(IntSumReducer.class);

    // Declaración de tipos de salida para el mapper
    job.setMapOutputKeyClass(Text.class);
    job.setMapOutputValueClass(Composite3Writable.class);
    // Declaración de tipos de salida para el reducer
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Composite3Writable.class);

    // Archivos de entrada y directorio de salida
    FileInputFormat.addInputPath(job, new Path( "weblog.txt" ));	
    FileOutputFormat.setOutputPath(job, new Path( "salida" ));
    
    // Aquí podemos elegir el numero de nodos Reduce
    // Dejamos 1 para que toda la salida se guarde en el mismo fichero 'part-r-00000'
    job.setNumReduceTasks(1);

		// Ejecuta la tarea y espera a que termine. El argumento boolean es para 
    // indicar si se quiere información sobre de progreso (verbosity)
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}

