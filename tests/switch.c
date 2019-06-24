int main(void) {
    int sw = 1;
    switch (sw)
    {
      case 1:
        {
            int a = 5;
            int b = 5;
            sw = a * b;
        }
         break;
      case 2:
         sw = 20;
         break;
      default:
            sw = 0;
    }
    printf("%d\n", sw);
}

