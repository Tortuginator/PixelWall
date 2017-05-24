import DBSC

dat = [200, 9, 63, 3, 3, 19, 3, 19, 3, 19, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 10, 0, 0, 0, 0, 2, 32, 14, 0, 0, 0, 16, 24, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 52, 58, 35, 0, 0, 0, 2, 20, 12, 0, 0, 0, 18, 30, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 53, 78, 81, 74, 18, 0, 16, 21, 0, 0, 0, 0, 0, 18, 38, 22, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 62, 80, 84, 78, 35, 0, 36, 43, 0, 16, 30, 0, 8, 46, 60, 44, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 45, 72, 72, 65, 26, 0, 12, 16, 0, 12, 19, 0, 36, 50, 64, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 46, 51, 36, 2, 0, 0, 0, 0, 0, 0, 2, 42, 60, 53, 12, 0, 0, 20, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 60, 46, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 2, 10, 2, 0, 0, 0, 12, 26, 26, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 38, 44, 36, 22, 0, 0, 6, 12, 6, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 29, 45, 60, 64, 49, 27, 0, 0, 14, 32, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 40, 61, 58, 56, 42, 22, 13, 18, 2, 2, 2, 12, 29, 25, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8, 32, 27, 2, 8, 45, 66, 62, 32, 0, 0, 26, 48, 19, 0, 8, 41, 69, 66, 36, 2, 0, 0, 0, 0, 0, 0, 0, 18, 46, 50, 42, 22, 30, 48, 44, 18, 0, 0, 10, 26, 4, 0, 14, 58, 84, 81, 62, 35, 7, 0, 0, 0, 0, 0, 0, 2, 27, 60, 60, 42, 6, 16, 16, 2, 0, 0, 0, 16, 29, 2, 10, 41, 79, 89, 86, 58, 22, 0, 0, 0, 0, 0, 0, 2, 42, 75, 66, 36, 8, 0, 0, 0, 0, 0, 0, 29, 46, 14, 0, 12, 58, 70, 75, 52, 16, 0, 0, 0, 0, 12, 32, 4, 45, 65, 56, 52, 38, 4, 0, 0, 0, 0, 0, 4, 14, 0, 0, 0, 25, 45, 38, 10, 0, 0, 0, 0, 0, 6, 14, 0, 10, 22, 46, 68, 56, 18, 0, 0, 7, 14, 6, 0, 16, 36, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 26, 48, 41, 18, 0, 2, 34, 53, 49, 25, 19, 42, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 22, 22, 12, 16, 30, 42, 68, 74, 48, 14, 0, 0, 0, 0, 0, 14, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 34, 46, 35, 40, 48, 32, 10, 0, 0, 0, 0, 2, 32, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 32, 38, 46, 16, 8, 0, 0, 0, 22, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42, 56, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 6, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 23, 0, 0, 0, 0, 4, 74, 33, 0, 0, 0, 37, 54, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 48, 115, 129, 80, 0, 0, 0, 4, 46, 28, 0, 0, 0, 41, 72, 26, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 121, 178, 189, 169, 41, 0, 37, 48, 0, 0, 0, 0, 0, 41, 88, 50, 0, 0, 0, 0, 0, 56, 0, 0, 0, 0, 0, 0, 141, 185, 193, 178, 80, 0, 82, 100, 0, 37, 69, 0, 20, 106, 138, 98, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 102, 165, 165, 148, 60, 0, 26, 37, 0, 26, 44, 0, 79, 114, 145, 62, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 104, 121, 84, 7, 0, 0, 0, 0, 0, 0, 4, 96, 136, 121, 28, 0, 0, 46, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 69, 136, 108, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 56, 0, 0, 0, 0, 0, 0, 7, 23, 4, 0, 0, 0, 28, 62, 60, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 88, 98, 79, 50, 0, 0, 13, 26, 13, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 66, 102, 136, 145, 112, 64, 0, 0, 33, 76, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 90, 135, 130, 125, 93, 53, 30, 41, 4, 4, 7, 28, 66, 56, 20, 0, 0, 0, 0, 0, 0, 0, 0, 20, 74, 64, 4, 20, 102, 152, 137, 71, 0, 0, 60, 105, 44, 0, 18, 94, 161, 152, 84, 7, 0, 0, 0, 0, 0, 0, 0, 41, 106, 114, 96, 50, 69, 109, 98, 41, 0, 0, 23, 60, 10, 0, 33, 132, 190, 189, 144, 80, 16, 0, 0, 0, 0, 0, 0, 7, 64, 136, 136, 96, 13, 37, 37, 7, 0, 0, 0, 37, 66, 7, 23, 94, 182, 204, 196, 130, 53, 0, 0, 0, 0, 0, 0, 4, 96, 173, 152, 84, 20, 0, 0, 0, 0, 0, 0, 66, 106, 33, 0, 28, 132, 158, 173, 115, 37, 0, 0, 0, 0, 26, 76, 10, 102, 148, 130, 118, 88, 10, 0, 0, 0, 0, 0, 10, 33, 0, 0, 0, 56, 102, 88, 23, 0, 0, 0, 0, 0, 13, 33, 0, 23, 53, 104, 154, 128, 41, 0, 0, 16, 33, 13, 0, 37, 82, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 62, 105, 94, 41, 0, 7, 75, 121, 112, 56, 44, 96, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23, 49, 50, 28, 37, 69, 96, 154, 169, 109, 33, 0, 0, 0, 0, 0, 33, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 13, 0, 78, 106, 80, 92, 109, 76, 23, 0, 0, 0, 0, 7, 76, 28, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 76, 86, 104, 37, 18, 0, 0, 0, 53, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 130, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 53, 0, 0, 13, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 53, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#dat = [200, 3, 39, 3, 1, 141, 1, 147, 0, 0, 1, 13, 2, 0, 10, 1, 24, 18, 52, 52, 40, 16, 1, 3, 0, 0, 0, 2, 10, 0, 1, 7, 13, 14, 2, 4, 0, 0, 2, 40, 68, 80, 66, 36, 2, 13, 16, 26, 19, 0, 19, 32, 14, 1, 6, 13, 34, 40, 19, 1, 3, 2, 38, 72, 0, 69, 40, 22, 0, 53, 52, 35, 2, 18, 24, 12, 1, 6, 18, 52, 62, 32, 30, 26, 0, 0, 19, 46, 62, 45, 26, 40, 64, 64, 50, 26, 0, 18, 22, 8, 1, 6, 14, 0, 0, 32, 0, 1, 6, 22, 16, 40, 74, 0, 22, 0, 0, 21, 0, 13, 1, 6, 2, 0, 30, 18, 1, 7, 26, 45, 40, 43, 38, 12, 1, 3, 13, 2, 1, 7, 2, 7, 1, 8, 29, 52, 46, 18, 8, 1, 18, 2, 1, 4, 16, 34, 38, 18, 1, 20, 32, 0, 6, 0, 4, 1, 18, 12, 0, 8, 8, 26, 32, 21, 2, 0, 0, 2, 2, 0, 8, 4, 1, 12, 2, 30, 46, 22, 16, 32, 25, 6, 0, 0, 7, 0, 0, 0, 32, 16, 1, 10, 4, 26, 27, 0, 53, 26, 8, 20, 0, 0, 0, 20, 32, 32, 14, 0, 12, 30, 0, 42, 26, 2, 1, 5, 2, 32, 61, 56, 49, 49, 32, 0, 1, 4, 36, 52, 45, 34, 2, 36, 62, 75, 69, 43, 14, 1, 5, 21, 50, 66, 53, 40, 38, 22, 1, 4, 6, 40, 56, 56, 35, 8, 48, 69, 84, 0, 44, 1, 6, 20, 40, 44, 0, 2, 6, 1, 6, 27, 42, 41, 22, 2, 34, 60, 62, 48, 10, 1, 6, 2, 27, 0, 0, 0, 8, 6, 1, 5, 2, 22, 24, 2, 0, 8, 22, 25, 8, 1, 8, 20, 32, 13, 16, 22, 1, 7, 22, 30, 2, 1, 13, 6, 12, 14, 36, 45, 22, 13, 0, 8, 14, 1, 3, 6, 1, 19, 22, 6, 1, 3, 21, 13, 6, 1, 4, 4, 22, 1, 11, 13, 22, 0, 14, 46, 53, 64, 53, 22, 1, 20, 2, 0, 43, 0, 87, 80, 45, 8, 0, 10, 0, 0, 2, 1, 17, 46, 72, 91, 87, 53, 1, 5, 22, 1, 18, 56, 75, 68, 38, 1, 23, 0, 12, 18, 20, 6, 1, 36, 22, 0, 1, 26, 6, 0, 1, 13, 4, 0, 23, 1, 24, 41, 118, 118, 90, 37, 1, 3, 0, 0, 0, 7, 23, 0, 1, 7, 30, 33, 7, 10, 0, 0, 7, 90, 156, 185, 152, 84, 4, 30, 37, 62, 44, 0, 44, 74, 33, 1, 6, 30, 78, 90, 44, 0, 74, 0, 7, 86, 165, 0, 161, 92, 53, 92, 121, 118, 80, 7, 41, 54, 26, 1, 6, 41, 115, 141, 76, 69, 60, 0, 0, 44, 106, 137, 102, 60, 90, 145, 145, 114, 60, 0, 41, 53, 20, 1, 6, 33, 0, 129, 72, 0, 1, 6, 50, 37, 90, 169, 154, 53, 0, 0, 48, 0, 30, 1, 6, 7, 53, 69, 41, 1, 7, 62, 102, 92, 100, 88, 28, 0, 0, 18, 30, 4, 1, 7, 4, 16, 1, 8, 66, 118, 104, 41, 20, 1, 18, 7, 1, 4, 37, 78, 86, 41, 1, 20, 76, 50, 13, 0, 10, 1, 18, 26, 0, 18, 20, 62, 76, 48, 7, 0, 0, 4, 7, 0, 20, 10, 1, 12, 7, 69, 106, 53, 37, 76, 56, 13, 0, 0, 16, 0, 0, 0, 74, 37, 1, 10, 10, 60, 64, 90, 121, 62, 20, 46, 0, 0, 0, 46, 71, 71, 31, 0, 28, 72, 0, 96, 62, 4, 1, 5, 7, 76, 135, 128, 116, 116, 72, 0, 1, 4, 82, 115, 102, 78, 4, 84, 141, 173, 0, 100, 33, 1, 5, 48, 114, 152, 121, 90, 88, 53, 1, 4, 13, 90, 128, 125, 80, 18, 109, 161, 187, 0, 98, 1, 6, 46, 90, 98, 0, 4, 13, 1, 6, 64, 96, 94, 49, 7, 75, 136, 141, 105, 23, 1, 6, 4, 64, 72, 0, 0, 20, 13, 1, 5, 4, 50, 54, 4, 0, 20, 53, 56, 20, 1, 8, 46, 76, 30, 37, 50, 0, 20, 1, 5, 50, 72, 4, 1, 13, 13, 28, 33, 79, 102, 53, 30, 0, 20, 33, 1, 3, 13, 1, 18, 82, 53, 13, 20, 0, 130, 48, 30, 13, 1, 4, 10, 53, 1, 11, 30, 49, 0, 33, 106, 121, 145, 121, 53, 1, 20, 4, 0, 100, 0, 198, 185, 102, 20, 0, 23, 0, 0, 4, 1, 17, 108, 165, 206, 200, 121, 1, 5, 53, 1, 18, 125, 173, 156, 88, 1, 23, 0, 28, 41, 46, 13, 1, 36, 53, 0, 1, 26, 13, 0]
#dat = [200, 3, 0, 3, 1, 123, 1, 126, 0, 0, 1, 35, 8, 1, 4, 2, 40, 30, 1, 3, 14, 22, 13, 1, 12, 25, 49, 56, 30, 1, 3, 2, 36, 29, 1, 4, 34, 18, 1, 12, 54, 79, 0, 72, 16, 0, 22, 32, 4, 2, 7, 0, 0, 22, 46, 25, 1, 4, 21, 13, 1, 5, 2, 1, 3, 75, 34, 0, 30, 46, 12, 32, 45, 2, 12, 49, 0, 0, 0, 1, 11, 42, 0, 0, 64, 0, 0, 4, 12, 0, 20, 26, 8, 0, 54, 60, 25, 1, 12, 10, 42, 52, 34, 1, 7, 12, 46, 62, 0, 14, 0, 0, 14, 16, 1, 10, 0, 1, 8, 2, 36, 0, 0, 18, 1, 20, 2, 1, 3, 10, 25, 25, 8, 1, 16, 10, 35, 36, 22, 18, 0, 0, 8, 16, 2, 2, 1, 14, 2, 21, 30, 48, 62, 60, 36, 20, 0, 0, 12, 0, 2, 1, 15, 16, 44, 58, 0, 60, 43, 20, 10, 10, 2, 0, 0, 13, 27, 29, 10, 1, 9, 29, 25, 2, 25, 50, 72, 58, 36, 2, 0, 13, 32, 16, 0, 0, 40, 72, 70, 44, 4, 1, 7, 22, 48, 53, 45, 26, 40, 52, 43, 22, 0, 0, 6, 18, 10, 0, 13, 53, 0, 84, 72, 42, 12, 1, 6, 10, 34, 62, 59, 38, 13, 25, 18, 1, 4, 18, 34, 12, 6, 36, 0, 91, 88, 63, 30, 1, 6, 0, 36, 65, 58, 30, 1, 7, 26, 48, 21, 0, 7, 56, 68, 74, 49, 18, 1, 4, 0, 22, 2, 44, 58, 46, 45, 34, 8, 1, 5, 2, 0, 2, 0, 0, 19, 41, 34, 7, 1, 5, 0, 4, 0, 13, 26, 40, 0, 58, 21, 0, 0, 4, 12, 2, 0, 19, 42, 1, 16, 30, 50, 45, 20, 0, 0, 32, 49, 42, 19, 18, 36, 12, 1, 15, 14, 0, 0, 14, 12, 27, 43, 66, 0, 46, 1, 5, 2, 0, 4, 1, 11, 8, 10, 0, 40, 58, 40, 43, 50, 36, 12, 1, 4, 4, 0, 10, 1, 14, 29, 46, 45, 43, 0, 10, 1, 6, 0, 1, 16, 2, 46, 58, 14, 1, 25, 12, 16, 1, 46, 0, 1, 18, 2, 0, 1, 26, 22, 2, 1, 34, 20, 18, 1, 4, 4, 90, 69, 1, 3, 31, 49, 30, 1, 12, 56, 112, 125, 72, 1, 3, 4, 82, 66, 1, 4, 78, 41, 1, 12, 124, 182, 0, 165, 37, 0, 49, 71, 10, 7, 16, 0, 0, 53, 106, 56, 1, 4, 48, 30, 1, 5, 4, 144, 0, 0, 173, 78, 0, 69, 104, 28, 71, 102, 4, 26, 112, 136, 0, 0, 1, 11, 96, 0, 0, 145, 0, 0, 10, 28, 0, 46, 62, 20, 84, 124, 138, 56, 1, 12, 23, 96, 118, 78, 1, 7, 28, 106, 144, 0, 31, 0, 0, 33, 37, 1, 10, 0, 1, 8, 4, 82, 138, 106, 41, 1, 20, 4, 1, 3, 23, 56, 56, 20, 1, 16, 23, 80, 84, 50, 41, 0, 0, 18, 37, 4, 4, 1, 14, 4, 48, 69, 109, 137, 136, 82, 46, 0, 0, 28, 74, 4, 1, 15, 37, 98, 132, 129, 136, 100, 46, 23, 23, 7, 0, 0, 30, 64, 66, 23, 1, 9, 66, 56, 4, 56, 112, 161, 130, 82, 7, 0, 30, 76, 37, 0, 20, 92, 165, 158, 98, 10, 1, 7, 50, 105, 121, 102, 62, 90, 115, 100, 53, 0, 0, 13, 41, 23, 0, 30, 121, 0, 193, 161, 96, 28, 1, 6, 23, 78, 141, 134, 88, 30, 56, 41, 1, 4, 41, 75, 28, 13, 82, 0, 206, 202, 139, 69, 1, 6, 0, 82, 148, 132, 69, 18, 1, 6, 62, 105, 48, 0, 16, 125, 154, 169, 116, 41, 1, 4, 0, 53, 4, 98, 132, 104, 102, 78, 18, 1, 5, 4, 0, 4, 0, 0, 44, 94, 78, 16, 1, 5, 0, 10, 0, 30, 62, 90, 0, 129, 48, 0, 0, 10, 26, 7, 0, 44, 96, 1, 16, 69, 112, 102, 46, 0, 0, 72, 112, 96, 44, 41, 84, 28, 1, 15, 31, 53, 0, 33, 28, 64, 100, 150, 0, 106, 1, 5, 4, 0, 10, 1, 11, 20, 23, 0, 90, 132, 92, 100, 114, 84, 26, 1, 4, 10, 0, 23, 1, 14, 66, 104, 102, 100, 0, 23, 1, 6, 0, 1, 16, 7, 106, 129, 33, 1, 25, 28, 37, 1, 46, 0, 1, 18, 4, 0, 1, 26, 53, 4]
#dat = [40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,10,10,10,10,10,10,10]
#dat = [4,5,3,7,10,20]
#n_file = open("new 1.text", "rb") # opening for [r]eading as [b]inary
#dat = in_file.read() # if you only wanted to read 512 bytes, do .read(512)
#in_file.close()
dat = list(bytearray(dat))
print "Original length",len(dat),len(dat)*8

a = DBSC.DBSC(dat)
#print a.CalculateShiftMode()

"""i = 0
counter = []
while(i < 3):
	i +=1
	a = DBSC.DBSC(dat)
	a0 = a.Compress()
	print "Result length",len(a0),
	counter.append(len(a0))
	dat = a0
print counter"""
b = DBSC.DBSC(dat)
b0 = b.Compress()
b = DBSC.DBSC(b0)
b0 = b.Compress()
print b.CalculateShiftMode()
print "old:",len(dat),"VS new:",len(b0)