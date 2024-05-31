{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 168,
   "id": "e18cb019-2661-4966-8e49-db6c9be76dd2",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>WKT</th>\n",
       "      <th>SA22022_V1_00_NAME_ASCII</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>POLYGON ((1756604.2013 5885189.7242,1756635.54...</td>\n",
       "      <td>Glenbrook</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>MULTIPOLYGON (((1731415.9144 5954113.3835,1731...</td>\n",
       "      <td>Te Kuru</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>POLYGON ((1756212.6659 5932045.2113,1756231.42...</td>\n",
       "      <td>Mairangi Bay South</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>POLYGON ((1755659.5735 5936900.8966,1755759.05...</td>\n",
       "      <td>Glamorgan</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>POLYGON ((1728600.2875 5959680.6266,1728610.74...</td>\n",
       "      <td>Kaipara Hills</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                                                 WKT SA22022_V1_00_NAME_ASCII\n",
       "0  POLYGON ((1756604.2013 5885189.7242,1756635.54...                Glenbrook\n",
       "1  MULTIPOLYGON (((1731415.9144 5954113.3835,1731...                  Te Kuru\n",
       "2  POLYGON ((1756212.6659 5932045.2113,1756231.42...       Mairangi Bay South\n",
       "3  POLYGON ((1755659.5735 5936900.8966,1755759.05...                Glamorgan\n",
       "4  POLYGON ((1728600.2875 5959680.6266,1728610.74...            Kaipara Hills"
      ]
     },
     "execution_count": 168,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# data manipulation\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import re\n",
    "\n",
    "\n",
    "# Read in file\n",
    "file_path = 'meshblocks-auckland.csv'\n",
    "\n",
    "# List the columns you want to import\n",
    "columns_to_import = ['WKT', 'SA22022_V1_00_NAME_ASCII' ]\n",
    "\n",
    "# Use the read_csv function with the 'usecols' parameter\n",
    "mesh_blocks = pd.read_csv(file_path, usecols=columns_to_import)\n",
    "mesh_blocks.head()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 169,
   "id": "85c28f5c-f882-4131-af55-62162fbe822e",
   "metadata": {},
   "outputs": [],
   "source": [
    "coordinates = row_strings = mesh_blocks['WKT'].astype(str).tolist()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 170,
   "id": "8e4c1610-0fb3-4aca-b8ca-5eaf0e18093f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# Converts EPSG:2193 format to standard lon, lat coordinates, series type\n",
    "def convert_epsg_to_stdlonlat(coordinates_list):\n",
    "    polygon_coords_list = []\n",
    "\n",
    "    def convert_long_lat_pairs(coords):\n",
    "        # Find all numeric values in the string\n",
    "        numeric_values = re.findall(r'-?\\d+\\.\\d+', coords)\n",
    "\n",
    "        # Convert numeric values to pairs of longitude and latitude enclosed in square brackets\n",
    "        pairs = [[float(numeric_values[i]), float(numeric_values[i+1])] for i in range(0, len(numeric_values), 2)]\n",
    "        \n",
    "        return pairs\n",
    "\n",
    "    for coords in coordinates_list:\n",
    "        # Convert coordinates to long/lat pairs\n",
    "        coordinate_pairs = convert_long_lat_pairs(coords)\n",
    "        \n",
    "        # Initialize an empty list to store coordinate pairs\n",
    "        polygon_coords = []\n",
    "        \n",
    "        # Loop through each coordinate pair\n",
    "        for pair in coordinate_pairs:\n",
    "            lon, lat = pair  # Extract longitude and latitude\n",
    "            polygon_coords.append([lon, lat])  # Append the coordinate pair to the list\n",
    "        \n",
    "        # Append the list of coordinate pairs for this polygon to the main list\n",
    "        polygon_coords_list.append(polygon_coords)\n",
    "    \n",
    "    return polygon_coords_list"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 173,
   "id": "3725276e-835b-43d8-8541-d1b685845bcc",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[[1756604.2013, 5885189.7242],\n",
       " [1756635.54, 5885165.789],\n",
       " [1756659.0855, 5885159.498],\n",
       " [1756669.5132, 5885154.7146],\n",
       " [1756679.2556, 5885140.7928],\n",
       " [1756678.4033, 5885138.1097],\n",
       " [1756680.3764, 5885131.7355],\n",
       " [1756689.661, 5885133.3829],\n",
       " [1756696.8602, 5885128.2988],\n",
       " [1756709.3353, 5885129.01],\n",
       " [1756728.7323, 5885125.7983],\n",
       " [1756742.2533, 5885115.6574],\n",
       " [1756753.6931, 5885110.3832],\n",
       " [1756767.7495, 5885097.8294],\n",
       " [1756778.9104, 5885083.9347],\n",
       " [1756780.2193, 5885080.2939],\n",
       " [1756776.6671, 5885071.3478],\n",
       " [1756778.7122, 5885059.0675],\n",
       " [1756773.9607, 5885050.7505],\n",
       " [1756774.6184, 5885045.9213],\n",
       " [1756781.5347, 5885033.1267],\n",
       " [1756770.7319, 5885007.8985],\n",
       " [1756769.4314, 5884975.4343],\n",
       " [1756761.6783, 5884968.8934],\n",
       " [1756758.1657, 5884959.8429],\n",
       " [1756759.0512, 5884957.7934],\n",
       " [1756769.3117, 5884951.3592],\n",
       " [1756773.2016, 5884942.2763],\n",
       " [1756786.8254, 5884943.1564],\n",
       " [1756796.0691, 5884938.4873],\n",
       " [1756799.3963, 5884934.6388],\n",
       " [1756794.1835, 5884923.3244],\n",
       " [1756793.7117, 5884912.3027],\n",
       " [1756786.0087, 5884902.6477],\n",
       " [1756787.4902, 5884900.4077],\n",
       " [1756790.2441, 5884900.3471],\n",
       " [1756796.7222, 5884904.4125],\n",
       " [1756804.1862, 5884917.6829],\n",
       " [1756812.8569, 5884926.9148],\n",
       " [1756814.8414, 5884931.8834],\n",
       " [1756811.071, 5884940.3925],\n",
       " [1756812.6717, 5884950.1853],\n",
       " [1756811.8176, 5884953.2127],\n",
       " [1756806.5154, 5884958.7999],\n",
       " [1756804.6661, 5884963.0723],\n",
       " [1756793.6761, 5884966.2589],\n",
       " [1756790.0883, 5884972.6503],\n",
       " [1756790.5155, 5884978.5784],\n",
       " [1756798.0543, 5884986.8047],\n",
       " [1756798.1499, 5884989.0726],\n",
       " [1756791.0848, 5885002.6228],\n",
       " [1756791.3092, 5885007.8333],\n",
       " [1756796.0668, 5885013.1406],\n",
       " [1756806.548, 5885014.1071],\n",
       " [1756825.638, 5885004.4487],\n",
       " [1756851.7418, 5884997.6414],\n",
       " [1756860.2629, 5884989.6246],\n",
       " [1756866.4143, 5884986.0748],\n",
       " [1756892.3242, 5884983.8845],\n",
       " [1756906.3298, 5884975.142],\n",
       " [1756915.8351, 5884971.7203],\n",
       " [1756919.994, 5884972.2254],\n",
       " [1756926.2358, 5884970.274],\n",
       " [1756933.1863, 5884952.5767],\n",
       " [1756940.959, 5884921.9799],\n",
       " [1756955.8775, 5884905.5177],\n",
       " [1756958.0445, 5884897.4083],\n",
       " [1756961.7714, 5884893.8815],\n",
       " [1756959.1241, 5884880.6806],\n",
       " [1756959.5585, 5884875.2377],\n",
       " [1756974.5098, 5884856.1018],\n",
       " [1756977.6925, 5884848.164],\n",
       " [1756977.8286, 5884833.4757],\n",
       " [1756987.6401, 5884817.9059],\n",
       " [1756986.7238, 5884795.603],\n",
       " [1756990.4066, 5884790.6693],\n",
       " [1756991.8164, 5884784.1908],\n",
       " [1756983.041, 5884768.9529],\n",
       " [1756988.3814, 5884755.2718],\n",
       " [1756989.7892, 5884744.9513],\n",
       " [1756986.293, 5884728.3829],\n",
       " [1756989.7169, 5884719.1716],\n",
       " [1756999.309, 5884711.771],\n",
       " [1757004.2391, 5884695.7761],\n",
       " [1757003.3009, 5884679.763],\n",
       " [1756992.8432, 5884657.4254],\n",
       " [1756991.9784, 5884649.6316],\n",
       " [1756997.6627, 5884637.8013],\n",
       " [1756997.7666, 5884616.3156],\n",
       " [1757001.313, 5884607.1668],\n",
       " [1756998.8402, 5884587.3698],\n",
       " [1757001.8493, 5884539.9026],\n",
       " [1757004.2188, 5884529.4652],\n",
       " [1756980.8748, 5884525.1554],\n",
       " [1756879.4631, 5884488.1291],\n",
       " [1756906.6812, 5884413.5917],\n",
       " [1756900.6676, 5884368.054],\n",
       " [1756788.0851, 5884263.2993],\n",
       " [1756665.4231, 5884155.6766],\n",
       " [1756542.2362, 5884042.5903],\n",
       " [1756502.6525, 5884010.8141],\n",
       " [1756424.5249, 5883940.2534],\n",
       " [1755963.4179, 5883526.1893],\n",
       " [1755955.3886, 5883520.7757],\n",
       " [1755960.2407, 5883507.9387],\n",
       " [1756035.5116, 5883352.6863],\n",
       " [1756238.5784, 5883288.5318],\n",
       " [1756766.1788, 5882698.4961],\n",
       " [1756466.5116, 5882609.2023],\n",
       " [1756397.6993, 5882570.391],\n",
       " [1756380.1116, 5882555.5772],\n",
       " [1756346.0884, 5882519.0579],\n",
       " [1756339.5637, 5882532.448],\n",
       " [1756199.7976, 5882768.7809],\n",
       " [1756083.8767, 5882812.663],\n",
       " [1755957.7847, 5882909.7293],\n",
       " [1755586.1997, 5882725.1975],\n",
       " [1755403.6901, 5882752.8726],\n",
       " [1755382.1983, 5882783.5621],\n",
       " [1755366.7499, 5882785.3736],\n",
       " [1755342.076, 5882813.5784],\n",
       " [1755344.4774, 5882827.6518],\n",
       " [1755348.5412, 5882853.1189],\n",
       " [1755361.0496, 5882885.1523],\n",
       " [1755361.8466, 5882892.165],\n",
       " [1755322.0363, 5882916.108],\n",
       " [1755307.6249, 5882920.636],\n",
       " [1755303.6494, 5882924.9511],\n",
       " [1755294.5178, 5882964.3023],\n",
       " [1755288.6753, 5882972.505],\n",
       " [1755274.5318, 5882986.02],\n",
       " [1755266.5422, 5882998.0136],\n",
       " [1755255.2733, 5883045.549],\n",
       " [1755245.5962, 5883060.4225],\n",
       " [1755244.5753, 5883065.1713],\n",
       " [1755246.9116, 5883083.2563],\n",
       " [1755245.909, 5883100.7056],\n",
       " [1755252.988, 5883118.2721],\n",
       " [1755255.1893, 5883134.1787],\n",
       " [1755262.2811, 5883163.4209],\n",
       " [1755269.0577, 5883166.6107],\n",
       " [1755275.8297, 5883165.4535],\n",
       " [1755290.8615, 5883167.4975],\n",
       " [1755308.7463, 5883176.2388],\n",
       " [1755311.2392, 5883179.7981],\n",
       " [1755309.9601, 5883183.2216],\n",
       " [1755300.7764, 5883187.1463],\n",
       " [1755289.4907, 5883195.294],\n",
       " [1755282.9498, 5883205.1244],\n",
       " [1755269.4977, 5883210.5707],\n",
       " [1755265.3723, 5883214.9495],\n",
       " [1755262.5475, 5883225.4086],\n",
       " [1755263.144, 5883231.5834],\n",
       " [1755261.2592, 5883243.3349],\n",
       " [1755262.1587, 5883289.8262],\n",
       " [1755271.1232, 5883362.4673],\n",
       " [1755272.0653, 5883387.9293],\n",
       " [1755275.6822, 5883400.1027],\n",
       " [1755292.9428, 5883439.9527],\n",
       " [1755310.0969, 5883463.8463],\n",
       " [1755316.5373, 5883465.5624],\n",
       " [1755319.6788, 5883470.6599],\n",
       " [1755337.2681, 5883482.0389],\n",
       " [1755350.1379, 5883486.0761],\n",
       " [1755357.0045, 5883486.5857],\n",
       " [1755365.8312, 5883490.5607],\n",
       " [1755384.9032, 5883487.4207],\n",
       " [1755396.1364, 5883481.5362],\n",
       " [1755431.4054, 5883455.829],\n",
       " [1755453.3576, 5883461.0154],\n",
       " [1755463.3216, 5883458.1398],\n",
       " [1755478.0651, 5883448.474],\n",
       " [1755497.4639, 5883438.6759],\n",
       " [1755523.3472, 5883428.1696],\n",
       " [1755546.2565, 5883421.0054],\n",
       " [1755553.632, 5883415.7358],\n",
       " [1755559.1842, 5883414.1625],\n",
       " [1755570.2422, 5883416.8234],\n",
       " [1755538.6547, 5883429.4849],\n",
       " [1755505.0472, 5883448.7263],\n",
       " [1755470.1594, 5883464.7764],\n",
       " [1755459.553, 5883471.7371],\n",
       " [1755436.2931, 5883491.6639],\n",
       " [1755403.4409, 5883498.7025],\n",
       " [1755397.0884, 5883496.6205],\n",
       " [1755374.5072, 5883508.3455],\n",
       " [1755358.3756, 5883521.0778],\n",
       " [1755343.6453, 5883529.3058],\n",
       " [1755317.199, 5883549.5871],\n",
       " [1755306.3353, 5883568.2006],\n",
       " [1755282.0828, 5883588.8297],\n",
       " [1755269.4288, 5883605.7984],\n",
       " [1755259.6182, 5883611.3032],\n",
       " [1755253.196, 5883619.4832],\n",
       " [1755249.667, 5883635.1811],\n",
       " [1755228.0948, 5883685.7403],\n",
       " [1755226.3465, 5883692.7815],\n",
       " [1755229.9802, 5883725.7576],\n",
       " [1755229.7427, 5883738.4757],\n",
       " [1755232.2883, 5883753.8654],\n",
       " [1755236.6093, 5883760.7983],\n",
       " [1755247.1955, 5883768.0299],\n",
       " [1755254.2578, 5883779.8531],\n",
       " [1755252.605, 5883781.6464],\n",
       " [1755235.9566, 5883785.0225],\n",
       " [1755226.6704, 5883784.0709],\n",
       " [1755210.0242, 5883787.2471],\n",
       " [1755197.5742, 5883793.3147],\n",
       " [1755184.4591, 5883802.4024],\n",
       " [1755158.7954, 5883822.8055],\n",
       " [1755154.8327, 5883829.2068],\n",
       " [1755136.7303, 5883845.4878],\n",
       " [1755113.8417, 5883879.8703],\n",
       " [1755112.4283, 5883890.5512],\n",
       " [1755116.6926, 5883900.5134],\n",
       " [1755121.6591, 5883905.4385],\n",
       " [1755132.8633, 5883912.0725],\n",
       " [1755142.1553, 5883923.5272],\n",
       " [1755151.8446, 5883921.8558],\n",
       " [1755167.1032, 5883930.0206],\n",
       " [1755186.4211, 5883928.7598],\n",
       " [1755199.4474, 5883932.4171],\n",
       " [1755201.3176, 5883933.9882],\n",
       " [1755200.5738, 5883938.3546],\n",
       " [1755187.5215, 5883951.8307],\n",
       " [1755179.5863, 5883953.3496],\n",
       " [1755170.0107, 5883949.3937],\n",
       " [1755159.6292, 5883950.7764],\n",
       " [1755136.8878, 5883962.2483],\n",
       " [1755122.5256, 5883960.1491],\n",
       " [1755116.9437, 5883956.1214],\n",
       " [1755109.8553, 5883954.0378],\n",
       " [1755095.8176, 5883956.6976],\n",
       " [1755089.9346, 5883959.4587],\n",
       " [1755077.067, 5883972.441],\n",
       " [1755068.5173, 5883978.5309],\n",
       " [1755059.9324, 5884015.9627],\n",
       " [1755053.5166, 5884034.6437],\n",
       " [1755053.7225, 5884056.2567],\n",
       " [1755058.0072, 5884075.9114],\n",
       " [1755057.7724, 5884088.6313],\n",
       " [1755053.8127, 5884105.7373],\n",
       " [1755050.2445, 5884112.7509],\n",
       " [1755048.8015, 5884125.0491],\n",
       " [1755044.7796, 5884134.6793],\n",
       " [1755044.2653, 5884151.4332],\n",
       " [1755050.5928, 5884159.206],\n",
       " [1755063.1671, 5884168.2863],\n",
       " [1755068.4885, 5884175.8408],\n",
       " [1755070.3497, 5884183.6645],\n",
       " [1755079.3818, 5884201.9739],\n",
       " [1755081.6299, 5884214.3225],\n",
       " [1755086.6722, 5884229.1389],\n",
       " [1755087.4871, 5884242.6756],\n",
       " [1755102.5553, 5884277.0262],\n",
       " [1755111.686, 5884288.4747],\n",
       " [1755127.64, 5884303.2584],\n",
       " [1755132.2826, 5884303.5317],\n",
       " [1755140.2663, 5884297.7962],\n",
       " [1755144.5917, 5884299.2537],\n",
       " [1755151.8967, 5884305.3602],\n",
       " [1755159.0736, 5884307.0888],\n",
       " [1755161.2223, 5884312.434],\n",
       " [1755154.8962, 5884320.7231],\n",
       " [1755145.9032, 5884326.1515],\n",
       " [1755140.924, 5884335.1594],\n",
       " [1755122.038, 5884383.9188],\n",
       " [1755116.4216, 5884409.2684],\n",
       " [1755103.9781, 5884431.4827],\n",
       " [1755095.5532, 5884455.3728],\n",
       " [1755089.201, 5884461.5331],\n",
       " [1755079.8612, 5884464.6188],\n",
       " [1755078.0091, 5884467.0114],\n",
       " [1755076.4766, 5884475.2638],\n",
       " [1755084.1126, 5884492.3411],\n",
       " [1755085.0357, 5884498.41],\n",
       " [1755089.9841, 5884505.5533],\n",
       " [1755104.0592, 5884510.4161],\n",
       " [1755108.4056, 5884517.3467],\n",
       " [1755115.4047, 5884522.2695],\n",
       " [1755116.7613, 5884526.3196],\n",
       " [1755116.2803, 5884531.5486],\n",
       " [1755110.0361, 5884543.7281],\n",
       " [1755108.6581, 5884554.9837],\n",
       " [1755111.1241, 5884565.8983],\n",
       " [1755116.121, 5884569.8055],\n",
       " [1755118.283, 5884573.8685],\n",
       " [1755119.5364, 5884584.7648],\n",
       " [1755118.4963, 5884600.4536],\n",
       " [1755112.2852, 5884624.3159],\n",
       " [1755103.5203, 5884643.1013],\n",
       " [1755097.7348, 5884651.6652],\n",
       " [1755078.2191, 5884659.3982],\n",
       " [1755067.6823, 5884661.2386],\n",
       " [1755060.1389, 5884665.7468],\n",
       " [1755052.7519, 5884673.2785],\n",
       " [1755045.0653, 5884687.449],\n",
       " [1755038.8888, 5884695.2024],\n",
       " [1755029.676, 5884703.1062],\n",
       " [1755007.0152, 5884732.3342],\n",
       " [1755000.2764, 5884737.0569],\n",
       " [1755002.2517, 5884753.8038],\n",
       " [1755000.8601, 5884779.7581],\n",
       " [1754997.3329, 5884799.6363],\n",
       " [1754990.4782, 5884812.2098],\n",
       " [1754992.725, 5884824.3291],\n",
       " [1755004.3663, 5884830.6056],\n",
       " [1755014.8369, 5884830.6237],\n",
       " [1755031.7103, 5884826.0842],\n",
       " [1755055.7362, 5884829.3209],\n",
       " [1755061.7328, 5884832.122],\n",
       " [1755074.0638, 5884842.6514],\n",
       " [1755079.0961, 5884844.3752],\n",
       " [1755100.7508, 5884860.556],\n",
       " [1755121.2098, 5884883.4162],\n",
       " [1755135.3048, 5884888.1194],\n",
       " [1755142.8412, 5884896.5581],\n",
       " [1755144.5525, 5884903.147],\n",
       " [1755143.8355, 5884910.5871],\n",
       " [1755146.6144, 5884914.0561],\n",
       " [1755161.9228, 5884917.529],\n",
       " [1755184.2533, 5884910.8483],\n",
       " [1755194.4436, 5884904.9741],\n",
       " [1755222.3215, 5884904.83],\n",
       " [1755227.0027, 5884903.4876],\n",
       " [1755232.5251, 5884898.5486],\n",
       " [1755239.6264, 5884898.6414],\n",
       " [1755245.1473, 5884894.1038],\n",
       " [1755269.8257, 5884863.9259],\n",
       " [1755279.8573, 5884855.2299],\n",
       " [1755289.4434, 5884841.0852],\n",
       " [1755298.8817, 5884833.0493],\n",
       " [1755306.7362, 5884832.4826],\n",
       " [1755330.4218, 5884844.3042],\n",
       " [1755340.1366, 5884846.8404],\n",
       " [1755356.1753, 5884845.8489],\n",
       " [1755368.1852, 5884841.5983],\n",
       " [1755388.015, 5884825.618],\n",
       " [1755406.9041, 5884823.4639],\n",
       " [1755415.8607, 5884820.3739],\n",
       " [1755432.0772, 5884805.5239],\n",
       " [1755456.1655, 5884798.2625],\n",
       " [1755473.8288, 5884789.9414],\n",
       " [1755489.5659, 5884775.8344],\n",
       " [1755513.0148, 5884748.4754],\n",
       " [1755521.9125, 5884733.555],\n",
       " [1755528.0022, 5884715.9933],\n",
       " [1755532.7685, 5884689.7878],\n",
       " [1755529.8344, 5884680.3266],\n",
       " [1755523.277, 5884675.3756],\n",
       " [1755525.7508, 5884672.8271],\n",
       " [1755522.2107, 5884654.6053],\n",
       " [1755518.1358, 5884644.4456],\n",
       " [1755520.398, 5884642.0601],\n",
       " [1755519.5925, 5884631.9547],\n",
       " [1755521.6766, 5884627.5451],\n",
       " [1755536.7241, 5884620.9166],\n",
       " [1755544.4075, 5884620.6322],\n",
       " [1755558.0093, 5884616.2021],\n",
       " [1755571.2479, 5884608.9392],\n",
       " [1755583.9512, 5884596.8212],\n",
       " [1755606.9675, 5884584.0593],\n",
       " [1755617.4796, 5884569.6861],\n",
       " [1755622.0302, 5884557.3711],\n",
       " [1755622.6259, 5884512.4152],\n",
       " [1755621.3151, 5884504.9292],\n",
       " [1755625.3187, 5884491.6938],\n",
       " [1755623.0574, 5884479.956],\n",
       " [1755623.3562, 5884472.5013],\n",
       " [1755619.4809, 5884460.7342],\n",
       " [1755620.7874, 5884453.4995],\n",
       " [1755619.733, 5884441.7838],\n",
       " [1755622.3892, 5884423.8858],\n",
       " [1755627.82, 5884409.466],\n",
       " [1755629.437, 5884393.968],\n",
       " [1755643.164, 5884346.6309],\n",
       " [1755644.2398, 5884326.2835],\n",
       " [1755642.9774, 5884315.1691],\n",
       " [1755658.2408, 5884297.6873],\n",
       " [1755672.7995, 5884288.1966],\n",
       " [1755690.0686, 5884283.3636],\n",
       " [1755705.0911, 5884283.9033],\n",
       " [1755707.7377, 5884282.541],\n",
       " [1755711.8343, 5884278.9857],\n",
       " [1755721.5919, 5884263.2241],\n",
       " [1755727.828, 5884240.7445],\n",
       " [1755733.6749, 5884228.7494],\n",
       " [1755740.3842, 5884225.0403],\n",
       " [1755764.6764, 5884218.0239],\n",
       " [1755784.1524, 5884209.9089],\n",
       " [1755794.9311, 5884192.1528],\n",
       " [1755794.1503, 5884202.4282],\n",
       " [1755788.4918, 5884215.2337],\n",
       " [1755780.955, 5884220.1384],\n",
       " [1755761.293, 5884227.2412],\n",
       " [1755752.1298, 5884233.123],\n",
       " [1755746.9618, 5884240.6938],\n",
       " [1755727.4195, 5884287.5394],\n",
       " [1755725.1567, 5884290.121],\n",
       " [1755714.2861, 5884300.2113],\n",
       " [1755698.6285, 5884307.1881],\n",
       " [1755690.3784, 5884306.0292],\n",
       " [1755680.8414, 5884307.8723],\n",
       " [1755673.5314, 5884313.039],\n",
       " [1755667.0824, 5884323.7855],\n",
       " [1755661.9812, 5884341.1293],\n",
       " [1755664.9411, 5884406.7188],\n",
       " [1755661.1411, 5884434.8803],\n",
       " [1755663.1879, 5884462.9466],\n",
       " [1755672.27, 5884492.3534],\n",
       " [1755686.6255, 5884519.2338],\n",
       " [1755694.5945, 5884526.2359],\n",
       " [1755712.403, 5884536.0397],\n",
       " [1755720.8509, 5884533.6395],\n",
       " [1755735.5912, 5884524.6708],\n",
       " [1755742.261, 5884523.3746],\n",
       " [1755769.4993, 5884525.525],\n",
       " [1755777.0753, 5884530.8065],\n",
       " [1755772.1073, 5884542.7891],\n",
       " [1755747.7691, 5884562.8882],\n",
       " [1755735.1018, 5884570.3776],\n",
       " [1755712.5877, 5884577.4664],\n",
       " [1755704.2489, 5884582.9629],\n",
       " [1755698.5258, 5884590.3053],\n",
       " [1755687.1133, 5884600.5739],\n",
       " [1755667.364, 5884616.1354],\n",
       " [1755658.9818, 5884627.0526],\n",
       " [1755655.6773, 5884635.4342],\n",
       " [1755642.6005, 5884647.2003],\n",
       " [1755627.5134, 5884671.9375],\n",
       " [1755627.7662, 5884685.6084],\n",
       " [1755634.3529, 5884713.5908],\n",
       " [1755634.8225, 5884743.0699],\n",
       " [1755638.1374, 5884754.5422],\n",
       " [1755636.1684, 5884784.392],\n",
       " [1755635.8995, 5884825.0909],\n",
       " [1755637.5753, 5884838.1454],\n",
       " [1755635.2111, 5884849.3417],\n",
       " [1755644.4825, 5884872.3224],\n",
       " [1755646.9742, 5884884.9864],\n",
       " [1755646.679, 5884892.8017],\n",
       " [1755655.4179, 5884909.157],\n",
       " [1755668.6743, 5884924.6057],\n",
       " [1755675.2438, 5884929.8745],\n",
       " [1755687.3329, 5884936.1511],\n",
       " [1755695.632, 5884948.8944],\n",
       " [1755701.3727, 5884968.7367],\n",
       " [1755704.2075, 5884973.0534],\n",
       " [1755718.9118, 5884984.6609],\n",
       " [1755724.4642, 5884985.7568],\n",
       " [1755732.4462, 5884990.5519],\n",
       " [1755752.3943, 5885012.0142],\n",
       " [1755758.9692, 5885013.7313],\n",
       " [1755772.2337, 5885025.1193],\n",
       " [1755792.9449, 5885034.3679],\n",
       " [1755800.996, 5885033.4586],\n",
       " [1755808.1994, 5885034.5757],\n",
       " [1755822.6759, 5885030.9023],\n",
       " [1755841.2238, 5885031.5652],\n",
       " [1755851.5462, 5885030.279],\n",
       " [1755857.9817, 5885026.7007],\n",
       " [1755884.0515, 5885018.9074],\n",
       " [1755899.1668, 5885009.6041],\n",
       " [1755906.0582, 5885002.6655],\n",
       " [1755915.4508, 5884992.1029],\n",
       " [1755934.6738, 5884963.7666],\n",
       " [1755962.5186, 5884944.3234],\n",
       " [1755973.9743, 5884940.7778],\n",
       " [1755987.638, 5884939.0207],\n",
       " [1755992.9461, 5884936.2845],\n",
       " [1756004.4326, 5884925.609],\n",
       " [1756017.7235, 5884916.7629],\n",
       " [1756020.6186, 5884912.1901],\n",
       " [1756020.1762, 5884897.7476],\n",
       " [1756003.837, 5884872.068],\n",
       " [1755998.9295, 5884857.7674],\n",
       " [1755997.7869, 5884845.8739],\n",
       " [1755999.2237, 5884839.1325],\n",
       " [1756009.1547, 5884817.6238],\n",
       " [1756012.3118, 5884814.3225],\n",
       " [1756018.3643, 5884811.0989],\n",
       " [1756030.9083, 5884811.6452],\n",
       " [1756032.307, 5884813.8686],\n",
       " [1756031.2633, 5884817.4637],\n",
       " [1756024.534, 5884822.5848],\n",
       " [1756011.0253, 5884838.0351],\n",
       " [1756006.2811, 5884847.7939],\n",
       " [1756014.0746, 5884863.9814],\n",
       " [1756031.8622, 5884893.8461],\n",
       " [1756034.6584, 5884901.8206],\n",
       " [1756035.1864, 5884913.8513],\n",
       " [1756032.976, 5884929.9746],\n",
       " [1756025.8778, 5884940.6741],\n",
       " [1756002.3343, 5884953.6874],\n",
       " [1755992.124, 5884961.7365],\n",
       " [1755981.0303, 5884966.2096],\n",
       " [1755977.5484, 5884969.1617],\n",
       " [1755971.9688, 5884995.3548],\n",
       " [1755973.7187, 5885001.9946],\n",
       " [1755972.8043, 5885010.8038],\n",
       " [1755973.7715, 5885014.8258],\n",
       " [1755981.225, 5885019.5379],\n",
       " [1755996.454, 5885036.1815],\n",
       " [1756014.5473, 5885050.6557],\n",
       " [1756034.7884, 5885072.3784],\n",
       " [1756059.5278, 5885091.352],\n",
       " [1756063.557, 5885093.8116],\n",
       " [1756073.2966, 5885093.7401],\n",
       " [1756093.4592, 5885104.8351],\n",
       " [1756095.3203, 5885101.6522],\n",
       " [1756100.6027, 5885101.1195],\n",
       " [1756109.1736, 5885097.0223],\n",
       " [1756115.9892, 5885104.1287],\n",
       " [1756122.4353, 5885108.2249],\n",
       " [1756139.6251, 5885113.0781],\n",
       " [1756151.5953, 5885112.8301],\n",
       " [1756159.2783, 5885114.8963],\n",
       " [1756161.3226, 5885113.5339],\n",
       " [1756168.6177, 5885114.1607],\n",
       " [1756173.1327, 5885117.6619],\n",
       " [1756174.7036, 5885122.3034],\n",
       " [1756172.8304, 5885126.5022],\n",
       " [1756172.9813, 5885131.1276],\n",
       " [1756174.9798, 5885133.7635],\n",
       " [1756177.3923, 5885135.8053],\n",
       " [1756201.6491, 5885143.7423],\n",
       " [1756210.3742, 5885143.6488],\n",
       " [1756230.7237, 5885138.0731],\n",
       " [1756234.638, 5885132.895],\n",
       " [1756242.4123, 5885126.9608],\n",
       " [1756246.8299, 5885131.0353],\n",
       " [1756247.3932, 5885135.0631],\n",
       " [1756253.3986, 5885142.373],\n",
       " [1756278.2816, 5885148.7091],\n",
       " [1756292.3782, 5885140.04],\n",
       " [1756303.7909, 5885135.3571],\n",
       " [1756309.109, 5885131.4033],\n",
       " [1756316.5324, 5885120.8418],\n",
       " [1756326.4885, 5885119.3565],\n",
       " [1756339.227, 5885123.3338],\n",
       " [1756362.9724, 5885140.712],\n",
       " [1756379.1698, 5885143.5262],\n",
       " [1756396.5296, 5885151.3761],\n",
       " [1756407.4775, 5885152.1161],\n",
       " [1756413.9843, 5885150.791],\n",
       " [1756419.641, 5885152.8686],\n",
       " [1756454.887, 5885176.0189],\n",
       " [1756463.6042, 5885176.5284],\n",
       " [1756471.5718, 5885171.6022],\n",
       " [1756479.6804, 5885172.1044],\n",
       " [1756502.5366, 5885178.4166],\n",
       " [1756515.7816, 5885173.9564],\n",
       " [1756533.4157, 5885177.9941],\n",
       " [1756543.3779, 5885177.3131],\n",
       " [1756554.1305, 5885178.8538],\n",
       " [1756571.9273, 5885186.7101],\n",
       " [1756583.5001, 5885187.4567],\n",
       " [1756594.2019, 5885193.8208],\n",
       " [1756604.2013, 5885189.7242]]"
      ]
     },
     "execution_count": 173,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "polygon_corrrds_list = convert_epsg_to_stdlonlat(coordinates)\n",
    "polygon_corrrds_list[0]"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
