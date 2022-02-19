# Roll-able Table Pipeline

1. Count name occurrences.
   1. Split names where both the given and family name are represented in a single column (Mandarin)
2. Combine name counts.
   1. Combine names with the same pronunciation, spelt different.
   2. (Simplified pipeline) Transcribe everything into English
   3. ~~Combine English transliterations/transcriptions with the name in the predominant script of that country.~~
      1. ~~For transcriptions which may map to multiple possible names in their original script, distribute count proportionally between them.~~
3. Cull names to meet name count or percentage or representation.
4. Construct final table JSON
   1. ~~If in a script other than Latin, append string with an English transcription.~~
   2. Apportion *n* votes among each table based on their counts.

