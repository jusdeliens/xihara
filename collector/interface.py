from typing import Any

class ICollector:
	def reset(self):
		"""Erase every data collected"""
		...
	def collect(self, data:Any):
		"""Save the specified data for further characterization and model training"""
		...

