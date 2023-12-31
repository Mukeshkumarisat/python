{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "id": "TmJ9KSFXitwn"
   },
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import datetime\n",
    "import matplotlib.pyplot as plt\n",
    "import warnings\n",
    "from sklearn import pipeline,preprocessing,metrics,model_selection,ensemble\n",
    "from sklearn_pandas import DataFrameMapper"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "id": "JBR8S1c2itwy"
   },
   "outputs": [],
   "source": [
    "weather = pd.read_csv(\"Weather_Dataset.csv\",parse_dates=[\"Month\"], index_col=\"Month\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 450
    },
    "id": "lKQ4EeVoitw4",
    "outputId": "10364da8-399d-4fd9-cc9f-fa5b74cb1c78"
   },
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
       "      <th>Temperature</th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>Month</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>2010-01-01</th>\n",
       "      <td>21</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2010-02-01</th>\n",
       "      <td>24</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2010-03-01</th>\n",
       "      <td>30</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2010-04-01</th>\n",
       "      <td>33</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2010-05-01</th>\n",
       "      <td>36</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2019-08-01</th>\n",
       "      <td>29</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2019-09-01</th>\n",
       "      <td>29</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2019-10-01</th>\n",
       "      <td>28</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2019-11-01</th>\n",
       "      <td>26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2019-12-01</th>\n",
       "      <td>21</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>120 rows × 1 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "            Temperature\n",
       "Month                  \n",
       "2010-01-01           21\n",
       "2010-02-01           24\n",
       "2010-03-01           30\n",
       "2010-04-01           33\n",
       "2010-05-01           36\n",
       "...                 ...\n",
       "2019-08-01           29\n",
       "2019-09-01           29\n",
       "2019-10-01           28\n",
       "2019-11-01           26\n",
       "2019-12-01           21\n",
       "\n",
       "[120 rows x 1 columns]"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "weather"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 296
    },
    "id": "bJoIlqMVitxC",
    "outputId": "0cc47552-10f7-424f-b330-7d7e920d9078"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x175015f26d0>"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAXoAAAEGCAYAAABrQF4qAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjIsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+WH4yJAAAgAElEQVR4nOy9e3QkZ3nn/3n7LrWk1mikuUs9xozx3WN7PLYZj4jBgDHEXkiIIQlxfiyQ5AABQnIgYbPHWXbPbrIBAgkBnEDiHCAJAbxc4gAOsS0bfJtxBtvD2OPbaO4eSTNqXVp9f39/dL+tVqu6q6rV71utcX3PmTNSdVXXo6q3nvq+3+fyCiklPnz48OHj7EXAawN8+PDhw4de+I7ehw8fPs5y+I7ehw8fPs5y+I7ehw8fPs5y+I7ehw8fPs5yhLw2wAqDg4Ny69atXpvhw4cPH6sGe/funZRSDll91pGOfuvWrezZs8drM3z48OFj1UAIMd7oM1+68eHDh4+zHL6j9+HDh4+zHL6j9+HDh4+zHB2p0Vshn89z9OhRMpmM16a8bBGLxdiyZQvhcNhrU3z48OECq8bRHz16lN7eXrZu3YoQwmtzXnaQUjI1NcXRo0c555xzvDbHhw8fLrBqpJtMJsPatWt9J+8RhBCsXbvWn1H58LEKsWocPeA7eY/hX38fPlYnVpWjr0cqkyJT8BmmDx8+fDTDqtHorfDCmRdY07WGrf1btZ5namqK173udQCcPHmSYDDI0FC5AO3RRx8lEoloPb8b3HfffUQiEV796ld7bYoPHz46BKvW0ZdkiaIski1ktZ9r7dq17Nu3D4Dbb7+dnp4efv/3f1/7eRuhUCgQClnfuvvuu4+enh5Xjr5YLBIMBttlng8fPjoMq1a6KZQKAOSKOU/Ov3fvXl7zmtdw5ZVX8sY3vpETJ04A8Au/8At85CMfYXR0lAsuuIDHHnuMt73tbWzbto3/9t/+GwCHDh3i/PPP57bbbuPSSy/ll3/5l0mn07bf+0d/9Ee85jWv4bOf/Szf+973uPrqq7n88su54YYbeOmllzh06BBf/OIX+cxnPsP27dt54IEH+M3f/E2++c1vVu3u6ekByi+E66+/nl/91V/lkksuoVgs8gd/8AdcddVVXHrppXzpS18yeTl9+PChEauS0X/4Bx/m8ROPM5+fB6A30rvi79y+YTt/ceNfONpXSskHP/hBvvOd7zA0NMQ///M/84lPfIKvfOUrAEQiEcbGxvjsZz/LLbfcwt69exkYGODcc8/lIx/5CADPPPMMX/7yl9m1axfvfve7+eu//ms+9KEPNf3e6elp7r//fgDOnDnDww8/jBCCv/3bv+XP/uzP+NSnPsVv//ZvL5lxfPnLX274dzz66KM89dRTnHPOOdxxxx0kEgkee+wxstksu3bt4g1veIOfSunDx1mAVenooexsa382mRGSzWZ56qmneP3rXw+UpY+NGzdWP7/55psBuOSSS7jooouqn73iFa/gyJEj9Pf3Mzw8zK5duwD49V//dT73uc9x4403Nv3eW2+9tfrz0aNHufXWWzlx4gS5XK4lh7xz587qcT/60Y944oknquw/lUrx7LPP+o7eh4+zAKvS0f/FjX/BVHqKF6dfBOD8wfPpifQYO7+UkosuuoiHHnrI8vNoNApAIBCo/qx+LxTKklP9i0kIYfu98Xi8+vMHP/hBfu/3fo+bb76Z++67j9tvv93ymFAoRKlUqtqdyy1KXbXfJ6XkL//yL3njG9/Y6M/24cPHKsWq1+jBvE4fjUaZmJioOuR8Ps/+/ftdfcfhw4erx//jP/4j1113Ha961ascf28qlWLz5s0A3HnnndXtvb29zM7OVn/funUre/fuBeA73/kO+Xze8vve+MY38oUvfKH6+cGDB5mfn3f1N/nw4aMz4Tv6FhAIBPjmN7/Jxz72MS677DK2b9/OT3/6U1ffccEFF3DnnXdy6aWXcvr0aX7nd36HSCTi+Htvv/123v72t7N7924GBwer23/xF3+Ru+66qxqMfe9738v999/Pzp07eeSRR5aw+Fq85z3v4cILL+SKK67g4osv5rd+67eqsw8fPnysboharbtTsGPHDlm/8MiBAwe44IILqr+PT49zJnMGKSUDXQMk+5OmzWwZhw4d4i1veQtPPfWU16a4Rv198OHDR2dACLFXSrnD6jNbRi+EiAkhHhVC/EwIsV8I8SeV7bcLIY4JIfZV/t3U4PgbhRDPCCGeE0J8fGV/yiIKpQKhQIhIMOJZiqUPHz58rAY4CcZmgddKKeeEEGHgQSHEv1U++4yU8s8bHSiECAKfB14PHAUeE0J8V0r585Uani/lCQfCBANBI0VT7cTWrVtXJZv34cPH6oQto5dlzFV+DVf+OdV7dgLPSSlfkFLmgH8CbmnJUpamVNYy+mwxSydKUGcb/Gu8OvHUqae4/s7rSWVSntrx9Se/znu/+15PbQD4/R/9Pp975HOe2pAr5njT197ETw7/xMj5HAVjhRBBIcQ+4BRwj5TykcpHHxBCPCGE+IoQYo3FoZuBIzW/H61sszrH+4QQe4QQeyYmJpZ9HovFmJqaqjqbWkev2iH40AfVjz4Wi3ltig+X+PcX/p37Dt3Hf7z4H57a8f2D3+fvf/b3FEvePqv/8LN/4At7vuCpDS+eeZEfPPcDfvDcD4ycz1EevZSyCGwXQvQDdwkhLga+AHySMrv/JPAp4N11h1pVMVnSQinlHcAdUA7G1n++ZcsWjh49ysTEBBLJyemTLMQWiAQjTM5Psv/0fiLBzmkudjZCrTDlY3VhfHocgLHxMd56wVs9s2MiPUGhVODE3Am29HkzjtL5NBPpCSbSE5yaP8W6+DpP7BhPjS/5XzdcFUxJKaeFEPcBN9Zq80KIvwG+b3HIUWC45vctwPEW7CQcDlerNKfSU1z0jYv47I2f5dot1/Kmu97E/7v1/3HL+S2rQj58nLVQzmTs8JindkymJ4Hyi8crR384dbj68wPjD/BLF/6SJ3aol68pR+8k62aowuQRQnQBNwBPCyE21uz2VsAquvgYsE0IcY4QIgK8A/juSo2eSJelnaHuoWpapakL5sPHaoN6Nvad3OepTj8xP7HEHi+gHCyUZzie2aEY/XSHOHpgI3CvEOIJyo77Hinl94E/E0I8Wdl+PfARACHEJiHE3QBSygLwAeCHwAHgG1JKdyWkFlADZrB7kKHuIbpCXcYumA8fqw3j0+Oct/Y8SrLET4+4K+xrF6SUVYLm5bOqHOx5a8/zdIaj7Dg6c3RJ8acuOMm6eUJKebmU8lIp5cVSyv9R2f4uKeUlle03SylPVLYfl1LeVHP83VLK86SU50op/1c7jFZTwKH4EEIIRhIjPqP34cMC87l5phamuPWiWwkHwp6x2LncXLXexWtGHwqEeMdF7+BnJ3/GdGbaMzsAirLI8dmW1GxXWJUtEGqlG4Bkf9J39D58WEA9F+cPns+OTTs8Y7Hqma21yQuMp8rxgevPuR6JNJbeaGXH+vj68s8GZjir09HXSDcAyUTSl258+LCAei6SiSSjyVEeO/YY6XzauB1qFt4d7vZcukkmkly9+WrPZjiFUoFjM8cYTY5WbdKNVenoJ9OT9EZ6iYbKLYCTiSQT6QlPBrAPH50M5USS/WVHny/leeToIzZHtR+KnG3fsJ3x1LhnxXfj0+Mk+5N0hbvYuXmnJzOcYzPHKMoiu0d2V23SjVXp6CfSEwzFh6q/q8yb2tQpHz58LGrSG3s2smt4FwLhCYtV0s2VG68knU8ztTBl3IZ8Mc+x2WMkE2V/MZocZc/xPcznzLbjrpXThrqHfEbfCJPpyapsA1RvnFdTwn0n93Hfofu479B9PPHSE57YUCwVefHMi56cuxaz2VlOzZ/y2gyOzhyt3pMHDz9Ivmjdh183XjzzIiVZ8uTcUHYqw33DBANBErEE2zds94TFKulmx6Zyc0UvntVjs8coydISR18oFXj46MNG7ajKaf1JY/HFVenoJ9IT1UAswEhiBCg/3Kax/9R+Lv/S5Vx/5/Vcf+f1XPbFyzyZWXz9ya9z3l+d5/ms5mP//jFu+IcbPLUB4IZ/uKF6T3b/3W6+8p9fMW7DidkTnPdX5/GN/d8wfm6F8dT4khberx5+NY8de8y4HRPzE0SCES5ed3HVLtOodbBQvhYAjx03ez3U3z7cN2wsvrg6Hf38UukmEUsAMJOdMW6L6h/y7V/5Nn96w58C5QfcNPZP7KdQKnD/ofuNn7sWz595ngOTBzztZyKlZDw1zjsufgf/8Rv/QVAEPXkBHpw6SKFUYP+pFZeOtIzx6fEqgwXY0LOB2dys8RnORHqCwe5BT2ff1XhFxYa+aB+RYMR4iuX49Djr4uvoCneRTCQ5nDqsPWaxKh39ZHqSwa5F6UatFzuXm2t0iDaMHR4jmUjy1gveynUj1wGQypqvPqyWuXtY7Qfle6P6mXiFdD5NppBh+/rtXH/O9Qx2D1alA5Mw3c+kHrlijuOzx5c4+v5YP2B+jE6mJxnqHmKga4B4OO4pox9OLHZl6Y30GvcbKvMHyrOLhcLCkvRTHVh1jn4+N89CYWEJow8FQsRCMWZzs02ObD+klIyNj1XTpBLR8szCiyKMauMqj/uZVMvcPUyhq9ZZVMbIUHxI+4NkBdP9TOpxdOYoErlEuvFqjKoECiGEZ3Uv46lxNvRsIBZa7MDaE+nxxtFX7ompGc6qc/Tqga0NxoI3N+zg1EFOzZ+qOvoqW/Kgn8h4apygCHJw6iAn504aPz/Ulbl7WBRTX2cx2D3ojaM33M9k2fmnl0oV4N0YnZif8LzupZZJK/RGe40SRCklh1OHlzB6ZZtOrDpHX21/UBOMBW8cvZJJqow+5g1byhVznJg9wRvOfQNQ7srnBZRkAt4y+voxMtQ95Kl0Y6qfSaPzL2H0Ho1RJd1AxdF7JN3Ury1t2m+cmj9FppBZdPQ+o7eGYmu10g2UtTbT0s3Y4THWx9ezbWAbAPFwnKAIGtc/j6SOIJG89fy3Eg/HPdPpO6XMfZl00z1UHTcmYbqfSaPzD/ctatJeaPS5Yo5UNrWkZcnphdNGHWxJlpYwaYWeSA+zWXN+o/7l2x/rpzfS6zP6enSSdKP0eSHK66sIIUjEEuaj+JVBcu7AuVw7fK13/UzmO8TRW0g3pxdOG80EUo7lknWXAN5lmWzs2VitIAdvNPqpdLk4qla6AbPX5NT8KbLF7HLpxnAwtl5OMxWzWHWOvpF00xvtNftmnh7ncOpwtYxZIRFNGGf0S/qZjIzy5EtPcnrhtFEbYPHebOrd5Ll0Ew6Eq05tKD6ERBq9JsqxmOxnUo/6HHrwRqOvn2F5sYZEfQ69gmmCaCWnmYhZrDpHPzE/QTgQpi/at2S76RtWr88r9Mf6jTN6lSO+pW8Lo8lRz7ry1Za5e9nPROVsq5mWYpImA7LqnpjsZ1KP+hx6KBMigTA6Rqtya41Gr+wzhfoceoWeSI9RyXd8epy+aF/1hats8hl9HVT7A/UQK3jh6Ptj/dVKP4VELGE8o6F2ir5z804iwYg3/UwqD/SOTTs862cCy1tkKAdjUqdXTsxkP5NalGSJIzNHljm2gAjQG+01OutUMz11Tzb2biQcCHcEozcu3Vhk/iT7k0xnprUWfK46R1/f0EzBdDB27PAY141cRzAQXLLdC0ZfO0VXXfnuHzdfIaskE6VLe9WOoX6MqJ9NZt7UTtG9yBs/OXeSXDG3zLGB+TFaL90ERIDhxLBZR58aJxFNWCoBmULGWFaUlZxmYoazKh19fSAWzDJ6KSXPnX6OS9dduuwzrzT6WpZw1aarePLUk8alE+VgqxqsRzr9xPzSXkheSDe1U3RV5m4SKsvHahFu02N0Yn4CgWCga6C6bWPPRl6ae8mYDSfnTrKpd9Oy7b3RXsBcVf2p+VNsiG9Ysu38wfMBtDZEXHWOvjYftxa9kV5yxVx1uTKdyBazlGSp2nqhFqbZktUUfWv/VjKFjPEioWX9TDzKvKmXbqqO3qR0U1vmXgm2mXzx1uvitTA9RifTk6zpWkMoEKpu6432Mp831x44lU0t0cUVTLdPmc3OLptVXLzuYhLRhFa5ddU5+nq2pmDyhqkFTuKR+LLPEtEEs9lZY61praboXjWOWtbPxANGny/mOZM5s2SMRIIREtGEcemmWuZe6Wdi8vy16yrXw3Qcqb7bLJjPX5/OTDd19CZsKckS8/n5ZQQxGAhy3ch1WtOibR29ECImhHhUCPEzIcR+IcSfVLb/XyHE00KIJ4QQdwkhll/F8n6HhBBPCiH2CSH2rMTY6kNsMXhNOnq1UEF3uHvZZ/2xfiTSWCdNqzJ3L9LXYLGrqJf9TFQAuF7eM90GoVZO82KG06jeBLzR6OufWdPJE6lMqloVXIveiDnpRhFEKyVg98hunp58WttaDk4YfRZ4rZTyMmA7cKMQ4hrgHuBiKeWlwEHgD5t8x/VSyu1Syh0rMVblQVsNXqW1mXgzqxtm5ejVYDLFmBrl5YJ5Rj+Rnqh2FfWqzL0Rkx2Km2uDkMqkSGVTy/uZGLwfE/MThAKhai1BLUxr9PVSGphPnpjOTNMfbcLoDdiifJPyVbVQadq62pfYOnpZhnrdhSv/pJTyR1JKFap+GFge9WkzqtH7TpFuwsulGzU9NMWYGjWuMlFWXYt8Mc90ZnqxKMajxlWNtOmhbnMdLOtfvl4w+kZpyFAeH6lMyljMwEpuVYzehA1SSlJZa0Zv0m+oc1gx+is3XUlXqIsHDnvk6AGEEEEhxD7gFHCPlLJ+deF3A//W4HAJ/EgIsVcI8b4m53ifEGKPEGLPxIT1A9mozw0sTsFMvJlVEMmS0VcYlCnGNJ4aZ01szRKW4IV0Ui+ZJPuTTC1MGV+Ps5FkMdg9aCwYW//yrb54TTJ6C11cIRFNUJRFI8FQKaVlAkVPpIdCqWAkeSJTyJAr5iw1epNZN80cfSQYKbcv0RSQdeTopZRFKeV2yqx9pxCiWiUkhPgEUAC+1uDwXVLKK4A3Ae8XQoxa7SSlvENKuUNKuWNoyHqA1hde1MILRt9IoweDjN4iLxfMM+qG1Y+G5ZuG0k2lg6UJBlnP6L148TaqNwGzY3Q6M01RFi2lGzBDzBTpspKxTAZj1d+q/vZ6jI6Msu/kPi2yr6usGynlNHAfcCOAEOI24C3Ar8kGT5CU8njl/1PAXcDOVo3tOOnGKuvGtEZvUeYO5jXyegfrVS69euGs7Vq7ZPtg9yDZYtbI+BifHicajLIuvq66zYv7YUWIwOwYrS+WUjD5vKoXmiWjNxiMbcbogcX2JUfa377ESdbNkMqoEUJ0ATcATwshbgQ+BtwspUw3ODYuhOhVPwNvAJ5q1Vj1ENcWXiiYDMbaZd2AGbak1ka1dPQGyqprUS+ZeMno+2P9hIPhJduVozGh04+nxhlJjBAQi4+XFzOsRtKNyTHarAkhmHle1QvNSqNXz7DXwViAq7dcTTgQ1iLfOGH0G4F7hRBPAI9R1ui/D/wV0AvcU0md/CKAEGKTEOLuyrHrgQeFED8DHgX+VUr5g1aNnUxPsia2ZtlDDJ0j3ZjU6M9kzjCXm2so3YA5Rl0v3VT7mXiQ+WPl4NQ2E5k3VnLaSGKEM5kzRhybVS1BLUyO0fqW0QqdwuiDgSDd4e6OYPTd4W6u2nyVFkcfsttBSvkEcLnF9lc22P84cFPl5xeAy1ZoYxXNdEeTb+ZmWTfhYJiuUJcRtqTK6hsxeig7nUvWX6LdFuVA13aXJRMv+plA4zFisjr2cOowb9725iXbtvZvBeCFMy9w2Ya2PRKWaJaGDN4wei8dfTONHsw1NrNz9FDW6f/8oT8nU8gsWdt2pVhVlbGN+txA2bGYKsJolnUDi+lrunFm4Qyw6FxrYZzRpydYE1ta5j7UPWS8L34jbdqkdHNm4cyyGMEVG68A4JFj9Qlr7UcjXVzBpEZ/JlMeo/Vyq8lgbDNGD+ZaFatzNHP0rxx4JYVSoe2FU6vK0Tfqc6NgytGn82kCIkAkGLH8PBFLMJ3Vz5aaMYT1PeuJBCPGGLUVk/Zita1G2rQp6SZfzJMtZpfdk1cOvJINPRuMtI9uJJcomM66USSsFkYZfRONHsqauSlGHwlGGvoNqCEkbZ55ripH3yzABOaq7dL5NPFw3LIYBcwxejU4rdK1AiLASGLEmKO3egn3x/qNVmA2ytmGsmOJBCPapZvqPakLuAkhGE2Ocv/4/dpTPBsFQBVioRiRYMTIvUllUiSiiWXPitFgbDZFUAQtpVYw13dnNjvbMLVSQVen1VXj6NVD3IilgDlGP5+bbyjbQFkLNMGW7KaCJjM9JuaXy2qmroPCTHaGfClvOUaEEEaqY5vNskZHRjk6c1T7y9dOugFz/W6ms9OeV6ROZ8o2NCJmpvzGXH6uqWwD+maeq8bRq4e42eA1Jt0U0k0dvSkmaxfcMZm7bZXtYmpmU2sDNHZwJvrdNHX0lX4muuWbRrUEtTDV7yaVsW4P3BXqIiACxoKxjQKxYDYYa+voX+7STbNiKQVTC4Sn82nLYikFY4w+a8Po+5OcnDtJtpDVakdVMqnX6KMJFgoLRsrcoXkPdjDTwbJZ9eNF6y5iTWyNdkffqJagFsYYfWba0skKIYwFQRu1KFYwFozNzjbMoVdIRBOEAqGXr3RjF2CCzpFuTGr0XaGuZcsZKqjMmyMzR7TakcqmKJQKy+6NerhMsfpmLTKg0tjMkEZv9fINiAC7k7v1M/omfW4UTPWkb7TgB5h7Xhu1KDZthxNGL4RgsHvw5SvdNFtIQcFkMLapRh9LkC1myRQyWu2Yy801ZQim2hA0YtLq4TKl09tKN93eSjdQ1umfPf0sJ2ZPaLOhWRqyglFG3yjbxZBkYsfoeyNlJUB3kHw2Zx+MBT2dVleNo3ci3ZhMr2wUwQdzTHY2N9uUIZhqQ9DoJVy9DoYyb+yyTQa7B0llU1qlJLsy92rfcU3taAFLGa0eRjV6iz7wYE4ysdPoeyI9FGWRbFGvxOmE0YOeTqurx9G7kG50v5nn8/ZZN6CfydoNnC19WwiIgH5G36A1sKnrULVjfoJYKNbw3ijnN5We0maDHaO/fOPlxMNxrfLNxPziAjCNYILRl2SJmexMQ0ZvipjZMnpDrYqdOnodSQOrxtFPpifpCnU1DYL2RnopyRILhQWttthJN6aY7FxurulUMBwMs6l3k/50vgbSjWmNXmnTjdLodOUo18KuFW0oEGLXyC5tjr5RYLweiWiCdD5NvpjXYgeUZzcS2dDJmkieKMkSs9lZW0YP+nP6neTRgy/d2A5eU7m5dtKNKW3aTroBMymWatGR+lYMpjX6qYUpy3YQCuvj64Hyguq6oMZeMyIwOjLKk6ee1NIeopqGbBOMNUFG1H1v5GRNMPqZ7EzTl42yA/T6jUYV01YY7B7k9MJpCqWC7b5OsaocvV2AyVS1nZOsG9DPZJ1MBZP9+oumpjPThAKhZS8/0xr9dGaaNbE1DT8fTgwDi83gdGAuN0d3uLthJhQs6vQPHn6w7edvtih4LUz0u1H3vWHWTVi/o7drfwBm+u44aWimoF7S7SQCq8bR2/W5ATNvZiUNdYJG7yQvN5lIcmTmCMVSUZsdjcrceyI9CIQxRm+XRre5d7P2mIWT6flVm68iGoxqWQjaSXYamOl3U2X0TXrM6A7G2jU0AzN+o1FrDCvo6LS6ahz9xHxnSDcqZbJZrMCkRt8TtpduCqUCJ+b0pfNNZ62DXQERMJavDfZBt3AwzObezVqlLCdl7rFQjKu3XM3Y4fbr9HZFYwometKr+94sj34+N09JlvTZYNOiGMwEY10xeg2dVlePo0/bZxKYmII1W3REoSfSQ0AEjGTd2DJ6A7n0zZh0ImqmkyfYp9EB2tdudTLLAtg9spu9x/e23bk4lW6MMvomfeAlsvpM6bTBCaPXKfnaBelroaPfzapw9JlChrncXEcw+mbLCCoIIeiL9mllstlClnwp7ygYC3pz6ZsxaVNVwsVSkZnsTNMHGvQ3enOaQjeaHKUoizx05KG2nt+pdNMRGr2B59WJRm9SunEajIWXoXRjV9quYCIY22x1qVrobmzmdOCMJEYAzYy+CZM21ZNeMSZbRp9IcnTmaFszGmrh1NFfu+VagiLY9jRLVUvgZHyCoaybJnn0oNfBOmH0JpQAu75UtVB+7mXH6J3qjiYGjhPpBvQ3NnM6FYxH4gx2D3rG6E1VYDp5oKEs3RRlkeOzx7XY4bTMvTfayxUbr2i7Tq+y0xrVElTPX7FR5xhNZVJ0hboaLrRhgpg50ehjoZj2TppugrHhYJj+WP/LT6N3Oh01It3YLCOo0CmMHvTn0qusGyuY6qniZIoO+pdYdMrooSzfPHL0kbb2RHKSnQblRbF1y4vN+tyAOUbfFepq2slTddLsFOkG2t9p1dbRCyFiQohHhRA/E0LsF0L8SWX7gBDiHiHEs5X/LROYhRA3CiGeEUI8J4T4eCtGOg0wRYNRQoGQkWBss6wb0C9ZuGEIOnPpi6Uis7nZ5ozegEbvhtGDvpiF0+pHKDv6bDHLY8cea9v5ndSbKOgOlDfrXAmLswrdGr3dmFC2dEowFtrfgM8Jo88Cr5VSXgZsB24UQlwDfBz4sZRyG/Djyu9LIIQIAp8H3gRcCLxTCHGhWyOdSjcm3sxOpRvdQUg3mp9i9Dp6AM1kZ4DGTFrNbHT3H3IyRQe9MQsppStGf93IdUB7G5w5SUNW0D1GG/WiV6hmu2gkZo1WuLKyZS6vn9Hb+Q2FoXh7W2qH7HaQ5SdUXYFw5Z8EbgF+obL9TuA+4GN1h+8EnpNSvgAghPinynE/d2PkZHqSgAiwpqtx1aOC7o54TrJuQL9G71a6SefTTC1MOWZ7TmHHpBOxBCVZcpQKqtMOhe5wN0PdQ1oYfbaYpSiLjh39QNcAl6y7hM898jl+/OKPl3wWCoT436/731yx8QpXNjiVbkD/rDOVTTWtVG4m3YxPj3P7/bfz+Zs+79g5WtrglNE76LvzN3v/hlgoxrsue5drO2azs7YV07UY7Bpkz/E9rs/TCI40eiFEUAixDzgF3COlfARYL7rKMngAACAASURBVKU8AVD5f53FoZuB2lUvjla2WZ3jfUKIPUKIPRMTS99kqWyKvmgfAWFvru4e106zbtbF15HKpljI62mw1mxh8HroZLF2TNpEvjY41+hBXy69XYtiK3z02o+ybe02csVc9V+2kOVHz/+Iu5+929X57WS0eqyLr9Pa98dOo28WjP3qE1/l7/f9PT9+4cfLPnNtg80sD+z77kgp+eN7/5gv7f1SS3bYNSCsh+pg2a6ZsCNHL6UsSim3A1uAnUKIix1+v1Xo39JyKeUdUsodUsodQ0NLGcl8bt7WsSp0inSjgn66+qrYLQy+xBaNurQtozdQgVlrh5OHWlcuvduAG8Bt22/jgf/vgSX/Hnz3g3SFuly/HN28/EGvpAfNe9FDc0avspFWmn5qFyeotaWZ33j29LO8NP9Sy4TFScV0LYa6h8gVc21TJ1xl3UgppylLNDcCLwkhNgJU/j9lcchRYLjm9y2A67y2dKH5Gq210N361GnWje6gn6tgrMZMEzsmbYzRZ1N0h7ubZlcoJBNJDqcOt93BuXn52qGV1hFuxgQslfR0wI7RR4IRIsHIMgdbKBX46ZGfAqw4/dQpo7dbnU69cFolLE4rphXaXTTlJOtmSAjRX/m5C7gBeBr4LnBbZbfbgO9YHP4YsE0IcY4QIgK8o3KcK9j1f6+FCUYfDoRtHYruNL7Z7CwCQVeoy3bfga4B4uG4N4zeQAWmssOpZJHsT7JQWGh7z2+3jLoZWknPdfui0dkeI1PIkC1mbe+JVUxt38l9zOXmOG/teTx+4vEVPc9ONXo7v6EcfcuM3kWQHhZTyduVeeOE0W8E7hVCPEHZcd8jpfw+8H+A1wshngVeX/kdIcQmIcTdAFLKAvAB4IfAAeAbUsr9bo106+h1p1c6sWVz32aCIqiV0fdEemwLY6CcjaRLl+4Yjd5BnxsFXS/hVqSbRmglmO/2/DrbY1Rnejb3xMrBKqf6h9f9IYVSgYePPtySDepl4zTrppkSoGyay821VFXt2tF3t7exma2jl1I+IaW8XEp5qZTyYinl/6hsn5JSvk5Kua3y/+nK9uNSyptqjr9bSnmelPJcKeX/asVINxq97mCsXS96hVAgxOY+fZ0S3Wax6NKllTPqi/ZZfm5So3fyQIM+Wa2VYGwjtMLoXWv0Ghl9lQDY3BMryWRsfIxtA9v4pQt+iYAItKzT23XPrLdjPm/dSXN8epzx1Djn9J8DLKYUu4HTimkF49JNJ6CjpBsX8QKdDbScrC61zBZNzC0ejjeUskytMuV0ig6rhNG3kProprYCYE1sDT2RHk8kPYX657UkSzxw+AFGk6OLbSJadPRuAvTqmll10lR1Dje/6magNRlyNUg3nsONo++N9JLOp7UttOHGFp0tcd0OnGR/ktMLp9v+Ekxlmy/2EQvFiAaj2jV6N9JNf6yf3khv+xl9G4Ox/VH3xUxuXzRCCK0EAOydbG906Qz85xM/5/TCaXaP7AbKyy4+fPRhsoWsextsumfW2wHWqZ5j42MkoomqTa2QFjcV01BO344Go+akm07AfN6ZXAKLg1xlx7TdFofSDZSZ47GZY1o6JbrNy9XFYp0EQU30u3ETjNUVs2hnMLYVRu826wb0tcdww+hrnati72q5xWqbiOPu20TYdc+stwMapHqOj3HdyHUMdA0A7mVItxXTUB6jQ/H2LRK+Khy93WLctdC9iIAbW5KJcqfEYzPH2m6Ha+lGky7thEknYvo7WDZrrGYFHbLaXG6OgAgQC8VW/F39sX6yxayrhmetzCi0MXqHGn29dDM2PsaWvi1s7d8KLLaJaEW+caPRN2rH8NLcSzwz9QyjydGWZUi3FdMK7ex3Y9sCoRPgSrqpsJlnTz/bdImyzX2bHVXaWtmi3ux2qHWu6ud2oZVgLOhh9HYl980YfbaQJRqKrsgGp6l8tUgmkvzkyE+WbS+UCgREoKWxoabnTjKh7FANYmdSxHqcvThaiREkE4uSnjouW8gSCUZW9Hc4ZfS1wVgpJWPjY1x/zvXVc6/tXsvF6y5mbHyMP9r9Ry3Z4DSPHuCFMy8sGc8/fP6HQHlmUe3h71JSazVIP9g9yLGZYxxJlZsLbOrd5LiFQj063tEXSgVyxZxjR696a1x/5/VN9/vw1R/mMzd+xrU9bmSkJc61vX6e2eys7XqxtdjYu5FIMMLzZ55vqx2pTIpXDryy6T6NetLfdeAu3nXXu3jud59jQ8+GFdkAzqboClv7tzKdmeb0wuklL+4bv3ojrxx4JV98yxdd2+F2et4M1fqDbIr1PesdHTObnSUWihEKOH+sazNvLlp3ERPzE7zic6/g7275O375wl92b3gFqUwKgbC9HrWM/vkzz3Ni7kRVC1e4bvg6vv7U193b4HBWAVT7aL39X96+7LN4OM4VG6+oOmzdaa8Km3o3cc8L9zDyF+UWJr9x2W9w53+509V3KHS8o3faFljhda94HV9/29ebrkP5ybFP8tyZ51q2x6l0U+0xo2Fq7NapBESAKzdeyUNH27t03XRmummZO5RZ3ZGZI8u2f+/g95jPz3Pfoft4x8XvWJEN6jxOcdXmqwB46MhDvPm8NwNl53TvoXvJFt0H/sC9nNYMrdQftPKiqc2lv2jdRdx36D7mcnN87+D3VuToVbqr3cyoJ9JDppChUCpU5ZnXJF+zZJ/NfZuZyc5QKBVcvcTcZCFdvuFy/uXt/2LJ1i8YuoBIMLLk5esGrQbpP3n9J6svva8++VX+7dl/Q0rZ0kxr1Th6pyw6Eozwzkve2XSfrz751ZazQNzISF3hLtbF17VdLlHBHbdTwdHkKJ9+6NOu/gY7O+yybqBxT3r1YI+Nj63I0TttUVyLqzdfTTgQZmx8rOrof3rkp5RkqeXc5XZ26KyVbhyfP+8uQA/Lc+lr78lK4DQLqrYn/dj4GIPdg5w/eP6SfWoDpW5e5nO5OeLhuCMZTghh+2ILBULEw3HtPYgUhhPD/Ncr/isAEsl7v/denpl6Ztn1cYKOD8Y6bQvsBivJAnGTdQN6gl3pfBqJdM0QRpOj5Et5Hjn6SFvsyBQy5Iq5lrJujs8er8pIK3UqrTD6rnAXOzfvXNJLRdnRagCsndJNK4x+Nut+RrGhZwORYKQ6RtX1ODR9aEUN+ZxmQdU68bHxMUaTo8sYa6sJFu2cYSm00sO/HfUVKgup1Wel4x2907bAbtDqOqbFUpFsMetYRgI9ufStMoRdw7sQiLYtSO2USSdiCRYKC+SKueq2B8bLRShvu+Bt7J/Yv6LsglY0eig/PHuO76mSCVUYc3rhdEt1GG6rH5uhFZmglRlFQAQY7htmPDXO6YXTPPnSk7ztgrcBi/eoFTiZ6cFigPLAxAFenH6R0ZHR5fu0uBKVjjUQEjH3q3K1o2J628A21sfXn/2OvhMY/UJhwbUtOjoltsoQErEE2zdsb9uC1E6ZtFW2wtj4GD2RHn535+8C8ODhB7XbUY/R5Gi1l8pCfoFHjz1KIppAIlvq6Og1o2/1/CqX/ieHf4JE8v6r3k8imlgRIXDL6FXvfcVcrfZpxdGfLYxeCMFocvTsdfRO2wK7QSKaYDY72zT90gqtvHSSiSSZQoZT81ZdnFvDSiowd4/s5qEjDy1h163CKZO26nczdniMXcO7uGbLNcRCsRU5lVY0eoBXD7+62kvlkWOPkC/lq2XurcwwWpFOGqEn0oNAuHIqrUoVSl4cGx8jEoxw7ZZruW7kuhUtcei0rqHq6J+7m75oH5euv3TZPtWqVZfNCnVIN600m2tXxfRocpQjM0daivl1vKN3m3XjBP2xfiTSdXMiNcV3IyPpKFRqpQJSYTQ5ykJhgb3H967YDreMXu0/lZ7iqVNPMZocJRqKcs2Wa1bMHgMi4PpB6ov2VWc4Y+NjCAS3vOoWoLVmUm6rlZshIAKuq2NbPX8ykeTE7An+/cV/Z+fmnXSFuxhNjnJg8kDLBMUpo1f2Hpw6yK7hXZZ54ith9O26Hwomms01wkp0+lXj6NvK6Fvskd4qo4f2Fiq5bV5Vi93JcrpWO3R6Nxo9LF5vJdOogbt7ZDf/efI/W+oKqL43EU20lHameqnc88I9XLbhMrat3Qa4bw9bkiXm8/NtZZBuY0mtziiS/Ukkkn0n91U1cpXW14qkVpIlZrIzrhg9WMs2tfu4Dsa2cYal0Gr76HZUTF+87mL6Y/1np6PXlXUD7gsfWnL0Ohl9CwxhXXwd5w+e3xadvlVGPzY+RjQY5apN5Vz20eQoJVmqrirk2o6s8z439RhNjpIpZHjw8IOMjoxWqyLdSjdqnLbTsbiNJbWs0ScWq/mUs71y05V0hbpaciqz2Vkk0lUzsdpzL9tnJcFYHYw+k3IVc2tXxXRABNg9srulZ7fjHb2urBtwX/ig4gVuZKT+WD990b62MvqVBndGR0Z58PCDK+7w2apGP3Z4jGu2XFNtfXDtlmsJBUIr6jvuNuNGQfVSgbKjWdu9FnAv3axETmsENz2CcsUc+VK+NemmQkYCIsCrh18NlOtRrh2+trUeMy4qUtUYjoVi7Ni0o+k+nRCMTcQS5Ev5amKGaTtGk6McnDroelH3s65gyglMMnooM6Z7D93L/xz7n0u2hwNh3nPFe6rOxSlWGtwZTY5yx+N38Af3/AEDXQMMdA3w2zt+23V/l+nMNEERtH0Jq+v9rQPf4tjMMR4/8Tif2P2J6ufxSJwrN165or7jrTL6ofgQFw5dyM8nfs7u5O5yBWQ04Vq6aWeLYoX+WD+Hpg85O/8K5LwtfVsQCK7YeMVShj0yyp/c/yeuX6RusqDU2Ll2y7VEghHrfSrEyk0wVkqpLY8eyuTCqR9opx1q1vPA+AO8/aLl7RoaoeMdvWLRXWH7tVGdwqRGD2XW+IU9X+CP7/3jZZ9FQ1E+fM2HXX3fStnj617xOhLRBJ95eLHXz2hylIvXXezqe1SutN2UtDfay7lrzuXuZ+/m7mfvJhKM8Jbz3rJkn6s2XcWdP2utj0cqm6qu/tMKbr3oVh44/ADr4uuAsvN3K920s0WxQqOK4qbnb2FMRIIRXrP1Nbx525uXbL9q81VIJPsn9leZvhM47UUPEAwE2bl5J7dedGvDfQIiQDwcd8XoM4UMJVlqfx59dLGD5cbejY6OaWfs5vINlxMOhNl7Yu/Z5ejT+TRdoa6Wugk2QquMvpWsG4DP3/R5Pvemzy3ZJqVkzZ+ucczYajGXmyMcCDdkQHbY0LOB0x87TUmWuOf5e7jp6ze1FAh1yqQDIsDBDx6sprMKxLLsirXda5nNzVIsFV136FsJowf476/570t+H+wedM3o27m6lIIbjX6lM4p7b7t32ba1XeWZptvnxG1dwyPvsa/UtlvTtR467gfUMHoXsu98br5tWYPhYJjhxLDrmN+q0OjbKdtA6xp9q4xeCEEoEFryLxwMt1w1O5udXTFTCYgAoUCoOrtppX+/m1Wd1PlCgZClI1ff08oLx20veju00gd8JdJJIySiCWayM47qPXQ4tlZnvm40eqfojfYyl3fO6NWLr93B2FZ60rfbh7WyloKtoxdCDAsh7hVCHBBC7BdCfKiy/Z+FEPsq/w4JIfY1OP6QEOLJyn57XFmHu7bAThEOhukOdxuTbhqh1cUv5vLtC+60GuiClTPpWrTClGAxla9ddkDZ0XdCMFbVezi5Nzqko1Znvq1WKjeD27WgtTN6F76j7Y6+BYLoRLopAB+VUj4uhOgF9goh7pFSVkU1IcSngGZ/+fVSypaamaTzzhfjdoNW8mHbXaWbTCR55Jj7BmPtzA9WjsFt1SGUB/u5A+e2xY5WV+9RqXztZI9KunHTElZHMLb2mvRF+5qfX9OMAty/fN1o9E7hVrrRcT1gqUbvFPP5+bZmDaoCt1wx51i+tWX0UsoTUsrHKz/PAgeAzepzUX4SfgX4x5astoEO6QZaq3BL59NEg9GWV3mpR6sLdrczP7jjGH2LMkFbGX18iFwx1xKD1MGonVwTHTOKWChGJBhp6Z7EQrEVrxxWi95Ib2v3Q0NTM3D38tMh3UhkdeUpJ3Cl0QshtgKXA7U0dDfwkpTy2QaHSeBHQoi9Qoj3Nfnu9wkh9ggh9kxMLE6bdTn6VhZf1nHDwH3VbDvzclfi6N1o9HZohSnV7t9ujR7cVceq69fO2aeba6JDqhBCtDTznc5Mt/V+QIXRu5h16pJu4uE4QRH0VqNvoQjTsaMXQvQA3wI+LKWsjZi9k+ZsfpeU8grgTcD7hRCW5W9SyjuklDuklDuGhhbXbJzPtXfao9AKo29n9Bxar5ptZ15uLBQjKIKug7ElWWI2O+u5Ru9mAWinGOweBNwVTc1mZ4kEIy1nQlnBzTXRIR0pG1zfk2yqrfcD3Gv0uoKxQohyIZvDWY6Usu0+rBWC6MjRCyHClJ3816SU367ZHgLeBvxzo2OllMcr/58C7gJ2OrYOjYy+BaaSLnQOo2/XlFQI4fohgnJ2jES2j9G3qNFXGX0bNfqhuPs2CDrK7d1ck7ncHALR/gy1Fma+ahnBdqI30tsR6ZVQSXt12JM+W8wikW29L8OJYQSivYy+osF/GTggpfx03cc3AE9LKY82ODZeCeAihIgDbwCecmwdmjX6FrJu2mnLxt6NhANh14x+LjfnamFwO7Ti6NvNpFtZOg80afQtSDe6qzBtz5+dJR5xtmyeWxtamWXpYvROe8zoCsaCu0I2HZX9kWCEjb0b2y7d7ALeBby2Jp3ypspn76BOthFCbBJC3F35dT3woBDiZ8CjwL9KKX/g2Dr0pFdCi1k3bZ6CBUSgpeKHduTR16I32us666bdTFqlvHaCRt+KdKNlNSOXGr0up9YJGn1vtJeiLDpeuH0uN0dQBFfcMdIKbgrZqkWWbc4cdJuabZteKaV8ELDMMZNS/qbFtuPATZWfXwAuc2yNBdL5tDaNPlvMkilkHA8GHamebm9YsVRkobDQ1mvSEqNvcbGPZmiVPUJ7pZueSA/RYNS1dNPucRoNRYmFYo6uSSsLgztBKzNfXRo9lEmOk+dVvfhW2jHSColYgudOP+doXx2MHsrxvUePPep4/5dlZSy0VvWngzW5LX5QA6eddvRGWmf07XygW2GPM9kZosFoW4OgQgjXbRCcrpHqFk6viY7e627OXwtdWTfgPDtsNtfeWW8t3DB6bY4+keRI6ojjVfI62tHnijkKpYI2jR5aWHy5zayptvjBCVpplWyHlWj07XRura7eo+OBHooPuXP0bW7DoOC0VbGu69Af62c+P0+hVHC0f7ZQniW3m9G7LezTJWWBO42++ry2ebaXTCTJl/KcmD3haP+OdvQ6lhFUaCVvWwujd1n8oIMhtOLotTD6FjI8dARBwX2/m3YWj9XCKXvUdR3cznx19LmB1hi9LkffH+uvNuCzg07pBpynZq8KR98p0s1sbrb9jN7lDdNxTdymroFGjd6lHqyLuQ12D7oKxrazeKwWTtmjruvgduaro64BFitcnTp6HbNvBTcN+HRKN+A8NbujHb2OZQQV3DZsKpQKZAqZtj9MI4kRwPkNa7VVcjO0yui7w92Eg+G22dHqepw6HuihbufSjS65Apwzel3Xwe3MV0cWFLhfN1andOPGd2jLujkbGb2OrBu3DZt0FWAM9w0DHjP6aC/z+XnHgR3Qo0krjd7Vepy6pJv4EDPZGUexE11yBThfIFxXMNZtDyIddQ3QgnTT5hTkWrjpd6OL0fdEehjoGjg7GL1O6cYto9fVJCkairKxx3nxgy6NHhbZhxOsZEHuRkhEE+SKOTKFjONjdAUhVS69E51eR7xCwQmjl1LqY/QuK5Z1VCpDi8HYNhYV1sKN79Dpw5KJJIdnDjvat6MdfbvbAteiJ9JDQARcL9WmgzUl+53n0uu4Jq00NlvJgtyN0EomlC4mW62OdaDT62jLq5CIJcgUMmQLjQuFFgoLSORZrdG7HaO6s27A2SxHV9YNlGXfs4rR68i6cduZT2dJdTLhPJdexzVppSe9jiyTVvrd6GJubvrd6Gb00NzR6i73B+81+lgoRkAEHDn6kiwxn5/XmkcPzhl9QATaWuehoPyGE6lzVTh6HYwenOcog55+4wpuih90SjeuGL2GLJNWetLrlm6cBGR1a/TQ/JrokhWB6oInbjR6gWi7LUIIx9lhSoLUxuhdavTd4W4tFbrJ/iRzuTnOZM7Y7tvRjl5n1g24q3DTLd3kS3lOzp203VfHNXGbugaaGL1L9pgv5skWs55LNyYYfbNroqtFMUAwEKQ30uuK0fdF+9reXA2cZ4fpalGs4Gac6mrhAu5SLDva0evMugHnGQ1QM3g0sCaVYumkaEono3eTS68r6wbcZ0LpeKAHugYQCEfSjW6NHppfE53XAdxVLOvoc6PgtPmeTlIG7tac1tWUEWr8xoy931gVjl4no++EYOxA1wCAoylYOp+u6pXtglvpJlPIkC1mPdfodTPZeCTu6JpMZ6a1yBWw6Lyb2aHbsbmpWNbRi17BKaPXfT3A+dKGunp1wSIxclK41dGOfj4/j0BoaTUK7gawzoCXG21ax8BxG4zV0ecG3Gv0uh9op8vXpbIprXIFNJ9t6Ryb4JLRa+hFr+BYusnqm33X2uJkbOjoeFtrAzgjaB3t6HUGMgD6o84HcHVNUI3FW44q7dq8ojy4Z/S6NGm363HqDEKCc9amq88NOIuf6L4ObrLTdHSuVHDaZdUIo486GxvzOX3SzVnn6HVBrf3oJNtlLjdHd7ibYCDYdjvcaNM6rolbR6+jzw3UrMfpNG6imcm6YfQ65QrwVrpxI3Hq1Og7JRjrxhadPkzNFJzE1jra0esMZEB5AEuk48Gja+B0h7sdM1kdAyccDBMNRh0HY3VmmbhhjyakGydjQ6dc0R3uRiCavnB0xiqgcxh9T6TH0Rg1pdE7lm40JZMERIB42FkcqaMdvU59CzpjqTYoM1mnrGk+P6/lmrhpbKZLowd3erBu5uZ0eq7TuQVEwDYoPJebIxQIEQ1GtdigZll2hTklWWImO6NPxnIopZlw9E6fF91k1WkmUsc7et2MHhwuvqyxvzVUAsMOVpbXdU16o73M5d1JN1oYfcz5og5GgrEOGKROucKJHaoNhLZYVqyfQqlQzYJrhLncHCVZ0ipjOWm+p1vSU9/tZGzo9mFOXzgva0fvJp1PVwWmglNGr+uaOB24oK/MHVorYtN1X3rCzh4inYweKky2yUtY13qxCk47verqc6Og7rNd87253BzRYLStLbSX2eIivVKXdANtdPRCiGEhxL1CiANCiP1CiA9Vtt8uhDgmhNhX+XdTg+NvFEI8I4R4TgjxcTd/xHyu/RkmtXATBNUp3YBzHVTXNXE6cKH8QAdEQFtvFbfBWF1kwMm0WLdcAfYPs+6x6bS3i04CAM6TBnSTMmXLXG6uqZxVkiXtZNVprMAJoy8AH5VSXgBcA7xfCHFh5bPPSCm3V/7dXX+gECIIfB54E3Ah8M6aY22hndG70Oh1dUlUcKpNa2X0DvPoFYPVIRW4ZfTxcFxL/jo4e5h1yxVQeeE4kG50welqbDolPaipKbAZp7plVmVLURabttRWn60K6UZKeUJK+Xjl51ngALDZoR07geeklC9IKXPAPwG3ODy2ozR6nUuTgfPiLZ2O3k16pa6HORFNMJuddZTyOpvTt7gElNlSSZaaPsy65Qpwxuh1y4rggtFreuk5qRJWn+t29E7qG3R23621o+3plUKIrcDlwCOVTR8QQjwhhPiKEGKNxSGbgdpGDEdp8JIQQrxPCLFHCLFnYqLcSMpExBqclRDrZgn9URdZNzqkG4cZJqC3zF2lvDq5J7ofaCcMUrdcoexodm9msjMvC43eqXSjMxW63pZmY0N3U0ZwHkdy7OiFED3At4APSylngC8A5wLbgRPAp6wOs9hmOQ+WUt4hpdwhpdwxNFTuHKg7kBENRgmIgG02gc4VfBQSsYTtyvL5Yp5CqaCH0YedB2N1LYQN7hZtN+Xomz1IOlsUK9jpsLqzfpwyel2FdApOm+8ZYfQOZhe6e3VBm7NuhBBhyk7+a1LKbwNIKV+SUhallCXgbyjLNPU4CgzX/L4FOO7knFJK7dKNEILucLeto88VcxRKBSMBr2ZMVufAccvodTkWN4s66GZuTqbnOovHFOweZt1ZP05fvtqlG4fttE0FY+1s0d19FxYTBuxqHJxk3Qjgy8ABKeWna7ZvrNntrcBTFoc/BmwTQpwjhIgA7wC+68B+ssUsJVnS6uihfBPUcl+NoLvyEJwFhnUvrZgtZskX87b76lhGUMHNou3GpJsmDFJni2IFlRFl9TCXZInZ7KzWF01XqItwIGzP6DMposGotiaEjoOxmoPTS2xpMjZ0Pq+1dtjFkcAZo98FvAt4bV0q5Z8JIZ4UQjwBXA98BEAIsUkIcTeAlLIAfAD4IeUg7jeklPud/AEmAhmAI0avO18bnKV66rwmbvrdTGem6Y92AKPP6g/GQmcw+pIssVBYWPbZTHYGidQqHTntQaRzpgcug7GaFgav2uIiGKs7vRLsX34huy+SUj6Itda+LJ2ysv9x4Kaa3+9utG8zmLhI6vudOnoTKWzNHJxW6abmIVrTZRVXL0PljWtj9G41eo0PtBMGaUKjr30J1997E1k/6vudaPQ6r4MiOI6CsYakm2ZjwwRZdUrQOrYy1kTEWn2/rXRjoKTaSaqnzmviZloskR2h0XdCMHY6M61VroBF9mglE5jI+lHf7zWjjwQjRIKRpnJJrpgjV8x1RDDWSNbNanf0JgIZUH7bOpZuDKSwOWH0utIrwX7A6M6scKrRSyn159E7uCY64xUKzR5m3UVKCo4ZveYXjl0Ft3KuptIrPZdumpCAWnS8o+8E6cZEMNaNRq+T0ds5et2atFqP086pZAoZSrLkeTB2OquXxUJzHVZ3pouCk2Zzuhk9evt9twAAHcVJREFU2Fdwm3hWgepyns3GhgmyuuoZvYmItfp+J02SQG8wti/aB9hIN5qzbsCeGehsUayQiNo7FROLS0SDUYIiaM/oNbPYpozelEYfdcDoDVwLuzRgE/E0KAeobWcXBnyY0wB1xzp6U1k38bBz6Ubn4AkHw8TDcWfSjYZr4nTAmMgy6Y/127ZsNnFPhBC2jc1MsViwvjfGNPoOyLoBZ+0gQC8pc2pLOp8mFAhp7aLpNLbWsY7eZDDWVroxEIwF+4fJhHRjN2B0a/TgrO+PKeZm9zDrzjSB5jqsiawfKL9853JzFEoFy89zxRwLhQUj8YpmRYWmnlWw726qu7IfzgLp5vTCaQDWxBqn+rUDTrJu5nJzBESArlCXVlvsWhXrfPk5DcaaYvS20k3lgdbN3Oym5zprChTsGH1XqItIMKLVho095frI47PWhe1T6SkA1nat1WrHQNdA1TdY2rEwVd1PN+xIgM6FwRVWfTB2Mj2JQGi/YUq6aVZCrBqa6VrBR8GuVbFi9DpeOGpA2mbdmNLobWQCk4y+aR69gaybZrKazvVqa5HsTwIwPj1u+flEutyIcCg+pNWOoe4hJtOTDT9Xnw1167UD7MdGuqC3hQs4iyNBBzv6ifQEA10DBANBredRN6JZCbGJJklgL1mo3j86XjhqoWE7ZmCCQTpJ5TOVXdGMtSm5QrejjQQjhAIh66ybrL5OorVIJiqOPmXt6JWDHewe1GrHYPcgZzJnGrbqmJgvv3BMMHq72Z7uNa9hMY60qh29bnYAi46+mXyju3Olgp1kYaJts5M8eu2pfA6ybkzUNkDza2Kizw2UH+ZGLxxTjH4kMQI0YfQVB6ubSavvVxLNMjvSE6yJrdEaAFXoBOlG2bFqg7GT6Ukj0y/1xm0WkDWxYg3Ya/Qm1p+0GzAmMiv6Y/1ki1nbWRYYkm4azHJMxCsUGrUqNlGkBNAV7mJdfJ0to9cu3VS+v5F8M5meNEIQoXJPbPLoTTh6J8uAdqyjn5if0D4NhEVG38zRm2h7CosafaN4gYn1Jx0xegOpfNC8psBUMLbZwg6mMl6gMXs08eJVSCaSHJo+ZPmZ0uh1SybKJ6gZhJUdJvwGOEuv1J11o+xYtYx+Ij1hhNFXpZsmRVPGNPpoglwx15DJ6pZunCxiYIrRq3M1wlxujqAIEg1GtdrSLIXOKKNvICGZKFJSSPYnGzL6iflyTC0UsO2TuCIon9CI0U/Mm/EbUH5e5vPzDZe9NMXonTy3Hevop9JTRqZg6o3bVLox0N8a7Nsg6A7uOGEGJrJMnPS7MZUJ1RPpIZ1PW678ZUqjV3Y0ampmktEfTh22nHFOLkwaYdLKJ6gZxDI7DEm+sDibbEQSdROzWjtWpaMvlAoUZbGzpBsDwVi7VsXapRuHwVjdeeNOGb0JOU3dd6vxYaqhGFiztkwhQ7aYNSIdQdnRZwoZTs2fWvaZKSat8vStpBspJZNpMy8csC9WMirdrMY8elV9Z1K66YRgrF2rYt1RfCcLDetcGFzBiUZvSk5rVjFsqqEYWMdPTPW5Uajm0lvIN6ay5MLBMP2xfkvpJpVNkS/ljQZjoXE1uR+MtUHV0ZuQbipSSKP0ypIsMZ+bN8PobVoVm2D0zZhBtlDOhDGl0dtJNybuiV1DMYGoNqTTbUe9QzHRjqIW1Vx6ixTLyfQkg11mmPRQ95CldGMql1+h2dgolopkChk/vbIZlKPvBOlmIb+ARHaORq9xKjjQNcBMdsY+y8TAIhdgL92Y6mcCjRf96I32EhD6HyMr1mYyGAyNGb2STEwx6cHuQUtHbyqXX6FZx1e17KPugillh12/ro529J0g3ZiqwATvNfqrN1+NRPLw0YctPzclFfREegiIgG16pUnpptGiH6acrFVQ2EQ7ilr0x/rpi/YtY/TTmWkKpYIxBzsUt26DYKoNg0Kz/lCm1tMAZ0WDHe3oTTB6xZAbRc5Ntj1tptFLKbVH8V89/GoCIsDY+Jjl56Y0aSGEbfGY6WBsoxx2U7KJeuHUSoymGT2U5Zt6Rm9aMhnqHrIMxnaSdGOq+26tHc1g6+iFEMNCiHuFEAeEEPuFEB+qbP+/QoinhRBPCCHuEkJYjjYhxCEhxJNCiH1CiD1ODM+X8sTDcbrCertFQjm4EwqEGjN6g21P4+E4QRG0dHC5Yo6SLGmVbnqjvVyx8YqGjt6kJmzXsln3wuAKzYKxJhm9FXs0rdGDdS69aSY92D3IZHpyWZqnaemmWTDW1FKo4IyEOmH0BeCjUsoLgGuA9wshLgTuAS6WUl4KHAT+sMl3XC+l3C6l3OHgfOVpoKFBA8170psqtYcKk23g4ExNBUdHRnn46MNkC9lln5lkkHaNzUxlQtm1CDYlm1jpwZ4x+jrpxrSDHeoeIl/KL+tLP5GeoCvUZUQXh+Zjw6R00xZGL6U8IaV8vPLzLHAA2Cyl/JGUUq1C8DCwZQW2LoFJvQ/Kb91GWTemmmcpNGrRa2ppxdHkKNlilseOP7bsM5OacLNWxcVSkXQ+bUa6abboh6GGYmAtIaUyKQIiYOSFp5BMJEllU0vkRePSTYOiKZM59GAj3Rh6XmvtaAZXGr0QYitwOfBI3UfvBv6twWES+JEQYq8Q4n1Nvvt9Qog9Qog9mWzG6A1rxuhNBmOhMZM1tbTidSPXAVjKN53C6NVDZEpOg87R6GtlAnV+3dXBtbDKvPFCuoHlbRBM5fIrhINhosGoJQkw9bxCm4OxQoge4FvAh6WUMzXbP0FZ3vlag0N3SSmvAN5EWfYZtdpJSnmHlHKHlHIHAXODBpxJNybYI1S0aYtgrKmp4NrutVy87mJLR5/KlvPGTWUgNcq6MTnLUg9zvaOXUhrPuoHlGr0p6UjBKpd+Yr4smZhgr7AoEdUHZE01QqxFoz4zq066ARBChCk7+a9JKb9ds/024C3Ar8kGLRellMcr/58C7gJ22p2vUCoYK76A8lu3kXRjMhgLjZmsySj+6MgoPznyk2XrgypN2kTeeH+0MaM3GTcB68Zmc7k5SrJkjNFbBWNN9rlRsGL0kwvmcuihuXRjUvKFxk3vTD6vbQnGivK88MvAASnlp2u23wh8DLhZSmlJh4UQcSFEr/oZeAPwlN05S7LUcYzelFNppE2bjOKPJkeZy82x7+S+JdtN9T6HMqOfyc5YdgY0/fK1Ym0m+9woG2BprMDk/VBYF19HNBhdxuhNOtim0o1hR2/H6E31urGDE2q2C3gX8NpKiuQ+IcRNwF8BvcA9lW1fBBBCbBJC3F05dj3woBDiZ8CjwL9KKX/gxHiTN8zO0UeCEe2LLyvYafQmGMLu5G5guU5vkkH2x/qRSEv907Sc1qwq1ZR0YhWM9YLRB0SAkcTIMo3epGQSD8eJhWJLpJtMIcNcbs6XbhrAtnm0lPJBwCrac7fFNiXV3FT5+QXgMlsrLGA6GNuoYMpUGp9CIlpmssVSccl6uSaj+Jt6N/HKgVcyNj7G7137e9XtJloUK9S2Kq4/p+kAuWWfGcMNxVRQrz7rxrRGD8tz6SfTk5w/eL6x8wshyouELywyelMrXNWj0cpfJp/XUCBELBQjQ+MV2TqyMhbM3rB4ON6Q0ZvMrIDFFXrqWb3JKD7AZesv4+DUwSXbTDN6dc56VNm0wYyXhozekA3qYa7PutHdMtoKFw5eyJMvPUmumAPMSzdQ6XdTw+hN5/IrNFvLNx6OLyFruu1ohs519B0i3ZhO2WqkP5qcCkL5+tfbYFqjB+t2ENWH2mBPk3oJybRGD0slpJIsMZOd8YTR707uZqGwwOMnHmchv8B8ft64ZDIUX9rB0nQuv0Kjjq+m/YZdBlrHOnrj0k2DrBvTbKVRRoHJKL6yY2phakkwtFMY/UR6gqAIGg2Eeq3RKzsUo5/NziKRxjV6gN0j5RjOA+MPLEomhpl0PRExncuv0GgNB9Nxi9XJ6IVZphQPx8kUMpYZHibbr0LjHOF0Pk1ABLSvkaow2D1ISZY4vXAaqGGQphh9k+UEVQWkiTRP6IxFP2DpCmBe9LlRWN+znletfRVjh8eqDtY0k+506cZ0queqdPShQMhotZ9iyQv5hSXbpZTlN7PBnP5m0k13uNvYdalfhFnljXcKozfNluoDbtOZaSLBCLFQzKgdyql40eemFqPJUR4Yf4CX5l4CzDPpoe4hZnOz1Z5Mk+lJAiLAmq41Ru3ojfaSLWbJF/NLtpsu3rLLQOtYR28SytHXyzfz+XkyhUxHFIOYWmh4mR0VpmS697mdRm/ynvREesgVc9XgI5jtXFlrh9KDTd+PeowmR0llU9x76F7AA+kmvpSITKQnWNu11tgsT6FRvxvTOf2rktGHA2Gj51OZLPUBWS/0x1goRk+kpyGjNwXFRtQLxzSDjAQjdIW6LBm96WmxZUMxD4qVaiUkL4LBtRhNljuZfPtAuVDeC+kGFsen6VmeglWr4nQ+TTqf9oOxdvCK0dc7esVmPdEf08s1ehNVdgr10o0XmnCjls1eBbq8Llaykm680OgBRhIjJBNJnj/zPEERNC6Z1I9P07E0Baux4UUG0Kpk9J5JN3VFU15F8q1W0DEt3VQZ07w3jF6dq57RF0oFziyc8WRa7HWxUm1xjhfB4HooVr+227xkUi8tepHLD9Zjw4vAsO/oHUAx5U6QbsB6TUzT0k00FKU30lt92XmhCVv1/Tm9cBqJNDsttuhJ3zGM3iONHhYdvReSScdINxZjw4sqXV+6cYBVI90YqopVqH3hdAqj9+KeNGwRbFg2UUHhozNHOTF3gq5Ql7EeTFZQjt4LJj3QNUBABBifHufE7AlOL5zuHEbvQcqpHaM361EdwnQwtlHWzUR6gnAgTF+0z6g9VtLNXG6Orf1bjdpR+8LxSqM/NH1oyTYvZlmKLdXOLrxg9Ko9xvBnhgHY0te2Rd1awraBbWzs2cim3k3Gzx0QAdbH1/Pphz/Npx8uN9Xd0LPBuB1WY8ML6cYuvbIjHX13xJxEAc2zbobiQ0Zz+qE8QBYKC1W5RkrJ0ZmjvOEVbzBux/HZ40DZscVCMaIhMwVbUO5JXy/deBE3UY7s2MwxAPLFPOl82jij/7VLf41wMFzN2b50/aVGz18PIQR3/9rdrImZDcQq/Mvb/4UnXnoCKC8Q8ysX/YpxG+rHBpT9RlAEjcpqu4Z3Nf28Ix29qepPhYbSjUe6X20gNNmf5EzmDHO5ueqiD6YwFB+qPkipjHmpIhFLdIR0sy6+jlgoVu3Y6FVqY1+0j/dc8R6j57TD9g3bPTv3rpFd7Bpp7uB0Ix6Js7ZrrWXbZpMB6lcNvqrp5x2p0ZtGw6wbjyL59UVTapEHtYybKQx2laUbKSXTWfNSRX+sn0whU61+BG9S14QQS3qwe12s5KOzUN+22XRDMyfwHT2NGb1Xubn1OcJqEHnB6DOFDPP5eU/SCa363UykJ0hEE8aDkMlEsvrC9br9gI/OQu3YgMVeTJ0E39FTzvKJBCPW0o3BPjcK9TnsXjH62heO6b78YN0GwauHKJlILpNuvCpW8tFZUGNDLZvtlRLQDL6jr6C+VXG+mGc6M+0No6+XblLjdIW6vCszn5/wpLeLVWMzr6bFyf4kp+ZPsZBf8Bm9jyVI9idJ59NMLUwB3qxdawff0VdQv8qUumle3LBENEEoEFoi3ST7k+azf2peOJ4weivpxiO2pGZTh1OHfY3exxLUjg1Vue1LNx2K+lWmvCqWgnLwr7bf9vj0uHHZBpZKN6lMZzB6z6SbSnxkPDXuM3ofS1AdG9PjnlRuO4GtoxdCDAsh7hVCHBBC7BdCfKiyfUAIcY8Q4tnK/5bJtEKIG4UQzwghnhNCfLzdf0C7UC/deNXnRmGoe2iJdOOFo1cO9djMMRYKC+aDsXUavVofwEtGPz49Xp1h2JWd+3h5oDo2UuOeLYBiByeMvgB8VEp5AXAN8H4hxIXAx4EfSym3AT+u/L4EQogg8HngTcCFwDsrx3Yc4pGl0o1XfW4UVPuB+dw8k+lJ4xk3UM7bDgfCPH/mecA8g61n9LO5WXLFnCcv3819mwmKYJXR90X7jC387KOzMdA1QDwcZ3x63LO1a+1g6+illCeklI9Xfp4FDgCbgVuAOyu73Qn8F4vDdwLPSSlfkFLmgH+qHNdx6CTpRp13Ij3B4dRhwHzGDZQlpKH4EM+dfg4wn2XSE+lBIKoM2suHKBQIsblvM+OpcU/63PjoXAghqrn0XisBjeBKoxdCbAUuBx4B1kspT0D5ZQCsszhkM3Ck5vejlW1W3/0+IcQeIcSeiYkJq120ojvcvaRgSjmVtd1rjdsCi/1uvMqhVxjsHqw6etOMPiACrO9ZX+134/W0WOVLe9HnxkdnQ6VYrlpGryCE6AG+BXxYSjnj9DCLbdJqRynlHVLKHVLKHUND5h/k+qybifQEA10DxjtpKgx1D3Emc4bnT5dlEy8YvbLj2Gy5j4cXWSa7hnfxwOEHAG/av9ZCsTYvisd8dDYUCfBaCWgER45eCBGm7OS/JqX8dmXzS0KIjZXPNwKnLA49CgzX/L4FON66ufqwTLrxqM+Ngjr3f578T0KBkCcdAmGpU/WCxe4e2c2h6UMcTh32pP1rLZKJJMdmjjGZnvQZvY8lSPYnmVqY4tD0IU8qt+3gJOtGAF8GDkgpP13z0XeB2yo/3wZ8x+Lwx4BtQohzhBAR4B2V4zoO9Y7e9Lqk9VAOds/xPWzp2+JZ4K+2MtgLXVr1PH9g/IGOkG6KssjBqYO+Ru9jCdSMe++JvR3H5sEZo98FvAt4rRBiX+XfTcD/AV4vhHgWeH3ld4QQm4QQdwNIKQvAB4AfUg7ifkNKuV/D37FiLEuvnPe2MZFyZvsn9nsm24D3jP7S9ZfSF+1jbHyMyfQk0WDUdpEFXVBxkmwx6zN6H0ugxsb+if0dF4gFB22KpZQPYq21A7zOYv/jwE01v98N3N2qgaYQD8fJFXMUSgVCgRAT6Qmu3ny1Z/YoVlAoFTwLxNbaIRC2ixvoQDAQ5LqR6xg7PMa1W65lsHvQeIWwQu0L12f0PmqhxkahVOi4HHrwK2OrUB0sF/ILSCk961ypUHvukb4R7+yoDNq+aJ/xBaAVRkdGeXryac/Z0nBiMdzkM3oftdjQs6GauLFapZuXBWqXE0xlU56/mdd2LaZ1esnolWPthEWoHz32qKf3pDvcXT2/n3XjoxbBQJDhvjIR8Bl9B6N2OcFOSJEKB8NV1uilRq+ugZcM9spNV9IV6lpij1dQL12f0fuohxobXo9RK/iOvoLaxUe8ztdWUMzAU0avGKyHmnQkGOHa4WuX2OMV1EvX1+h91EONDa/9hhV8R19B7XKC1TJmj52KGjAjCe80elUZ7DWDHR0pyzdeP0TqYfb6evjoPFQdfQdKNx25OLgXiIfL0s2t37yVfCkPeD8FG+weZH18PbFQzDMbQoEQa2JrPNeklU7v9T1Rsyuvr4ePzkMnSze+o6/gyk1X8u7t72YmV+7usLl385IsCy/wuzt/lyPnH7HfUTP+9IY/5YKhCzy14bqR6/j4ro9z86tu9tSOt1/4dk7MnmDbwDZP7fDRebjlVbfw9Kuf5vKNl3ttyjIItc5hJ2HHjh1yz549Xpvhw4cPH6sGQoi9UsodVp/5Gr0PHz58nOXwHb0PHz58nOXwHb0PHz58nOXwHb0PHz58nOXwHb0PHz58nOXwHb0PHz58nOXwHb0PHz58nOXwHb0PHz58nOXoyIIpIcQs8EyTXRJAagWfO9lnEJhc4XesFjuc2GlnRzv+1tVihz823Nnhj432nqPRPkkppXWjHSllx/0D9th8fsdKPnf4HU1tOJvscGjniu7J2WSHPzY67550ih2dMjbq/61W6eZ7K/zc6T4vFztM2ODb4f4cnWDHy+medIodbR8bnSrd7JENeja8nGzw7ehMOzrBBt+OzrSjE2ywQqcy+ju8NoDOsAF8O+rRCXZ0gg3g2/H/t3euoVZUURz//fNq5aNMK7mmeemFSJmvSsvCEpGsKOqDXsTsQ4X5ofwSWBBpGpg9SJMyKaOkzNQellmUJZZUhmXX9xPJa1FqQVoklasPex+YTj7OOc6duZy7fjDMzN4z6/zPOnvW7JnZs04xzUFHc9DwP5plj95xHMdJj+bao3ccx3FSwgO94zhOlZNJoJfUXdKnkjZJ2iDpvljeSdJHkrbF+RmxvHPc/qCkWUW2+ktaJ2m7pJmSlIOGRyXtlnQwL19IaitpqaTN0c60PHTEug8kfRftzJbUKg8dCZtLJK3PyRcrJG2RtDZOZ+eko42kOZK2xjZyW9Y6JHVI+GGtpH2Sns7JH/UKcaMhtteS/u8vZQ0j4+dvkDS9VD+kQjljMSudgFqgX1zuAGwFegHTgYmxfCLwWFxuBwwGxgGzimytBgYBApYB1+egYWC0dzAvXwBtgWvjchvgs1J90QT+OC3OBSwGRuWhI9bfCrwGrM/JFyuAAc3gOJkMTI3LJwFn5vWbJOyuAa7J4VipAX4u+CDuPyljDZ2B74Gz4vrLwNBK2klFbSurDypy3jvAMMLbr7UJh24p2u6OImfVApsT6/XA81lqKKorO9A3hY5YPwO4K08dQGvC+N6ReegA2gOfxwOx5ECfsoYVVBjoU9axG2iXt45E3YVRk7LWEdvlXqAHoTMyG7g7Yw2XAR8n1scAz6bx+5QyZX6PXlId0Bf4CuhiZj8CxPnxLnPPARoT642xLEsNqZGWDkkdgZuA5XnpkPQhodd0AFiUk44pwJPAH5V8fkoaAF6Ktyoekkq7tZimjtgeAKZI+kbSQkldstZRRD2wwGKUy1KHmf0F3AOsA34gdARezFIDsB3oKalOUg1wC9C9XA2Vkmmgl9SecGk/wcx+q8TEEcrKajgpaEiFtHTERjMfmGlmO/PSYWbDCT2bk4HrstYhqQ9wgZm9Ve6+aWmIjDazS4Cr4zQmBx01QDdglZn1A74AnshBR5JRhHZaNim0jdaEQN8X6Ao0AA9kqcHMfo0aFhBus+4C/i7XTqVkFuijsxcDr5rZm7H4J0m1sb6W0CM8Fo2EBlygG+EMnaWGEyZlHXOAbWZW8kOuJtKBmf0JLAFuzkHHIKC/pF2E2zcXSVqRsQbMbE+cHyA8K7i8VA0p6thPuKopnPQWAv1y0FGwdSlQY2ZrytGQoo4+AGa2I15RvAFcmbEGzOxdM7vCzAYRbv1sK1XDiZLVqBsRLpU2mdlTiaolwNi4PJZw/+uoxEukA5IGRpu3H2+ftDWcKGnqkDSVkMVuQl46JLVPNPgaYASwOWsdZvacmXU1szrCw7CtZjYkSw2SagqjOWJwuBEoZ/RPWr4wwrOSIbFoKLAxax0J6qmgN5+ijj1AL0mFzI7DgE0Za0BxBFYcoTMeeKEUDamQxYMAwoFnhEumtXEaQXgSvZxwZlsOdErsswv4BThI6Mn3iuUDCAfPDmAWJT7cSVnD9Lh+OM4nZe0LwtWMERpswc6dOejoAnwd7WwAniH03jJvG4n6OsobdZOWL9oRRpYUfDEDaJXTcdIDWBltLQfOzes3AXYCPXOOG+MIx0oD4STYOQcN8wkn3I2UMTItjclTIDiO41Q5/mas4zhOleOB3nEcp8rxQO84jlPleKB3HMepcjzQO47jVDke6J0WhySTNC+xXiNpr6T3KrTXUdL4xPqQSm05TlPggd5pifwOXCzp1Lg+jPBSTaV0JLwA4zjNEg/0TktlGXBDXP7Pm5sx1/jbMXf4l5J6x/JJkuYq5JzfKeneuMs04PyYyOzxWNZe0iKFXPCvVprczHHSwAO901J5HRgl6RSgNyEjYYHJwLdm1ht4EHglUdcTGE7IYfNwTHUwEdhhZn3M7P64XV9CaopewHnAVU35ZRznWHigd1okZtZASJVQD7xfVD0YmBe3+wToLOn0WLfUzA6Z2T5CIqujpf9dbWaNZnaY8Np8XbrfwHFKpyZvAY6TI0sI6XuHEHKXFDhWOuxDibJ/OPoxVOp2jtPkeI/eacnMBR4xs3VF5SuB0RBG0AD77Ng5yA8Q/mbOcZol3stwWixm1kjIMFnMJMK/RDUQ8rqPPcI2STv7Ja1S+EPyZcDStLU6zong2Ssdx3GqHL914ziOU+V4oHccx6lyPNA7juNUOR7oHcdxqhwP9I7jOFWOB3rHcZwqxwO94zhOlfMvAloRULjfsMMAAAAASUVORK5CYII=\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "weather.plot(color='green')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "id": "1V6V5R7zitxJ"
   },
   "outputs": [],
   "source": [
    "X = weather.values\n",
    "train = X[0:70] # data for training\n",
    "test = X[70:] # data for testing\n",
    "predictions = []"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 34
    },
    "id": "2t-nvf0jitxT",
    "outputId": "01b869dc-4813-41a7-e096-354d1a4e5909"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "70"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "train.size # total no. of train data"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "fd2UaOsejaQ5"
   },
   "source": [
    "# **Auto-Regressive Model**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "id": "d2hfu_WeitxY"
   },
   "outputs": [],
   "source": [
    "from statsmodels.tsa.ar_model import AR\n",
    "from sklearn.metrics import mean_squared_error"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "id": "rYaIlMRDitxf"
   },
   "outputs": [],
   "source": [
    "model_ar = AR(train)\n",
    "model_ar_fit = model_ar.fit()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "id": "TrfQErtcitxl"
   },
   "outputs": [],
   "source": [
    "predictions = model_ar_fit.predict(start=70,end=100)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 867
    },
    "id": "8R-gwIouitxq",
    "outputId": "385363f4-694a-40fd-d1c6-d022b60a05cb"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([[26],\n",
       "       [21],\n",
       "       [21],\n",
       "       [25],\n",
       "       [30],\n",
       "       [33],\n",
       "       [35],\n",
       "       [34],\n",
       "       [30],\n",
       "       [28],\n",
       "       [29],\n",
       "       [28],\n",
       "       [24],\n",
       "       [22],\n",
       "       [21],\n",
       "       [24],\n",
       "       [28],\n",
       "       [32],\n",
       "       [35],\n",
       "       [33],\n",
       "       [28],\n",
       "       [29],\n",
       "       [30],\n",
       "       [29],\n",
       "       [24],\n",
       "       [21],\n",
       "       [21],\n",
       "       [24],\n",
       "       [29],\n",
       "       [33],\n",
       "       [35],\n",
       "       [34],\n",
       "       [29],\n",
       "       [29],\n",
       "       [29],\n",
       "       [30],\n",
       "       [26],\n",
       "       [21],\n",
       "       [19],\n",
       "       [22],\n",
       "       [28],\n",
       "       [33],\n",
       "       [35],\n",
       "       [33],\n",
       "       [32],\n",
       "       [29],\n",
       "       [29],\n",
       "       [28],\n",
       "       [26],\n",
       "       [21]], dtype=int64)"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "test"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 136
    },
    "id": "KhrWNHyeitxv",
    "outputId": "bdfb39f8-5c0e-4ede-accc-b749194670d9"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([25.04898106, 20.66568024, 18.8376725 , 20.94717278, 26.72094645,\n",
       "       30.94423858, 32.56670209, 32.19426158, 30.41357871, 30.25660949,\n",
       "       30.59755505, 29.04052977, 25.5889904 , 20.92845302, 18.96743558,\n",
       "       21.39228454, 26.00144303, 30.46273414, 32.29022598, 31.63971535,\n",
       "       30.79655539, 30.52723804, 30.58125208, 29.26821763, 25.49283551,\n",
       "       21.34605036, 19.47304808, 21.30745795, 25.82165134, 29.90248832,\n",
       "       31.74869574])"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "predictions"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 1000
    },
    "id": "RCXBZmxritx2",
    "outputId": "289a8179-28d6-4383-f180-1923f2a2dc2d"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[[26]\n",
      " [21]\n",
      " [21]\n",
      " [25]\n",
      " [30]\n",
      " [33]\n",
      " [35]\n",
      " [34]\n",
      " [30]\n",
      " [28]\n",
      " [29]\n",
      " [28]\n",
      " [24]\n",
      " [22]\n",
      " [21]\n",
      " [24]\n",
      " [28]\n",
      " [32]\n",
      " [35]\n",
      " [33]\n",
      " [28]\n",
      " [29]\n",
      " [30]\n",
      " [29]\n",
      " [24]\n",
      " [21]\n",
      " [21]\n",
      " [24]\n",
      " [29]\n",
      " [33]\n",
      " [35]\n",
      " [34]\n",
      " [29]\n",
      " [29]\n",
      " [29]\n",
      " [30]\n",
      " [26]\n",
      " [21]\n",
      " [19]\n",
      " [22]\n",
      " [28]\n",
      " [33]\n",
      " [35]\n",
      " [33]\n",
      " [32]\n",
      " [29]\n",
      " [29]\n",
      " [28]\n",
      " [26]\n",
      " [21]]\n",
      "[25.04898106 20.66568024 18.8376725  20.94717278 26.72094645 30.94423858\n",
      " 32.56670209 32.19426158 30.41357871 30.25660949 30.59755505 29.04052977\n",
      " 25.5889904  20.92845302 18.96743558 21.39228454 26.00144303 30.46273414\n",
      " 32.29022598 31.63971535 30.79655539 30.52723804 30.58125208 29.26821763\n",
      " 25.49283551 21.34605036 19.47304808 21.30745795 25.82165134 29.90248832\n",
      " 31.74869574]\n",
      "Haze\n",
      "Cloudy\n",
      "Cloudy\n",
      "Cloudy\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Cloudy\n",
      "Cloudy\n",
      "Cloudy\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Haze\n",
      "Cloudy\n",
      "Cloudy\n",
      "Cloudy\n",
      "Haze\n",
      "Haze\n",
      "Haze\n"
     ]
    }
   ],
   "source": [
    "print(test)\n",
    "print(predictions)\n",
    "for x in predictions:\n",
    "    if x>=35:\n",
    "        print ('Sunny')\n",
    "    elif x>=25 and x<=35:\n",
    "        print ('Haze')\n",
    "    elif x<=25:\n",
    "        print ('Cloudy')\n",
    "    else:\n",
    "        print ('Null')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 282
    },
    "id": "M10vTU_Aitx7",
    "outputId": "82ee6308-a17e-46aa-a69b-4493ed3eab06"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[<matplotlib.lines.Line2D at 0x1750258cd00>]"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.plot(test) # taken data as test\n",
    "plt.plot(predictions,color='red') # predicted data"
   ]
  }
 ],
 "metadata": {
  "colab": {
   "collapsed_sections": [],
   "name": "Weather_Prediction.ipynb",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3",
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
   "version": "3.8.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}