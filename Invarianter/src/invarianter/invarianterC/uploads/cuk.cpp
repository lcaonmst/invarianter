#include <bits/stdc++.h>
using namespace std;

const int N = 3e5 + 5;

int n;
long long a[N], b[N], c[N];
int best[N];
long long wart[N];

int main()
{
	scanf("%d", &n);
	for (int i = 1; i <= n; i++) {
		scanf("%lld%lld%lld", &a[i], &b[i], &c[i]);
	}
	int ile1 = 0, ile2 = 0, ile3 = 0;
	for (int i = 1; i <= n; i++) {
		pair<long long, int> koszt1 = make_pair(b[i] + c[i], 1);
		pair<long long, int> koszt2 = make_pair(a[i] + c[i], 2);
		pair<long long, int> koszt3 = make_pair(a[i] + b[i], 3);
		pair<long long, int> res = min(koszt1, min(koszt2, koszt3));
		if (res.second == 1) {
			ile1++;
		}
		if (res.second == 2) {
			ile2++;
		}
		if (res.second == 3) {
			ile3++;
		}
		wart[i] = res.first;
		best[i] = res.second;
	}
	if (ile3 > ile2) {
		for (int i = 1; i <= n; i++) {
			swap(b[i], c[i]);
			if (best[i] == 2) {
				best[i] = 3;
			}
			else if (best[i] == 3) {
				best[i] = 2;
			}
		}
		swap(ile3, ile2);
	}
	if (ile2 > ile1) {
		for (int i = 1; i <= n; i++) {
			swap(a[i], b[i]);
			if (best[i] == 1) {
				best[i] = 2;
			}
			else if (best[i] == 2) {
				best[i] = 1;
			}
		}
		swap(ile2, ile1);
	}
	if (ile3 > ile2) {
		for (int i = 1; i <= n; i++) {
			swap(b[i], c[i]);
			if (best[i] == 2) {
				best[i] = 3;
			}
			else if (best[i] == 3) {
				best[i] = 2;
			}
		}
		swap(ile3, ile2);
	}
	long long licz1 = 0, licz2 = 0, licz3 = 0;
	for (int i = 1; i <= n; i++) {
		licz1 += a[i];
		licz2 += b[i];
		licz3 += c[i];
	}
	long long new_res = 0;
	for (int i = 1; i <= n; i++) {
		if (best[i] == 1) {
			new_res += b[i] + c[i];
		}
		if (best[i] == 2) {
			new_res += a[i] + c[i];
		}
		if (best[i] == 3) {
			new_res += a[i] + b[i];
		}
	}
//	cout << ile1 << " " << ile2 << " " << ile3 << endl;
	
	long long res = 1e18;
	if ((ile2 > 0 && ile3 > 0) || (ile2 > 0 && licz3 == 0) || (licz2 == 0 && licz3 == 0)) {
		res = new_res;
	}
	else if (ile2 > 0) {
		long long diff = 1e18;
		if (licz3 == 0) {
			diff = 0;
		}
		int ind = 0;
		for (int i = 1; i <= n; i++) {
			if (diff > a[i] + b[i] - wart[i]) {
				diff = a[i] + b[i] - wart[i];
				ind = i;
			}
		}
		if (ile2 > 1 || best[ind] != 2) {
			res = new_res + diff;
		}
		else {
			int new_ind = 0;
			long long new_diff = 1e18;
			for (int i = 1; i <= n; i++) {
				if (ind != i && new_diff > a[i] + c[i] - wart[i]) {
					new_ind = i;
					new_diff = a[i] + c[i] - wart[i];
				}
			}
			res = new_res + diff + new_diff;
			new_ind = 0;
			new_diff = 1e18;
			for (int i = 1; i <= n; i++) {
				if (ind != i && new_diff > a[i] + b[i] - wart[i]) {
					new_ind = i;
					new_diff = a[i] + b[i] - wart[i];
				}
			}
			res = min(res, new_res + new_diff);
		}
	}
	else {
		long long diff1 = 1e18, diff2 = 1e18, diff3 = 1e18, diff4 = 1e18;
		if (licz3 == 0) {
			diff1 = 0, diff2 = 0;
		}
		long long ind1 = 0, ind2 = 0, ind3 = 0, ind4 = 0;
		for (int i = 1; i <= n; i++) {
			if (diff1 > a[i] + b[i] - wart[i]) {
				diff2 = diff1;
				ind2 = ind1;
				diff1 = a[i] + b[i] - wart[i];
				ind1 = i;
			}
			else if (diff2 > a[i] + b[i] - wart[i]) {
				diff2 = a[i] + b[i] - wart[i];
				ind2 = i;
			}
			if (diff3 > a[i] + c[i] - wart[i]) {
				diff4 = diff3;
				ind4 = ind3;
				diff3 = a[i] + c[i] - wart[i];
				ind3 = i;
			}
			else if (diff4 > a[i] + c[i] - wart[i]) {
				diff4 = a[i] + c[i] - wart[i];
				ind4 = i;
			}
		}
		if (ind1 == ind3) {
			res = new_res + min(diff1 + diff4, diff2 + diff3);
		}
		else {
			res = new_res + diff1 + diff3;
		}
	}
	printf("%lld\n", res);	
}
